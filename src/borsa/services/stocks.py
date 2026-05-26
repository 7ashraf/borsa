from __future__ import annotations

import asyncio
import time
from datetime import datetime
from functools import partial

import structlog
from fastapi import HTTPException, status

from borsa.data.symbols import EGX_SYMBOLS, is_valid_symbol
from borsa.exceptions import AllFetchersFailed, SymbolNotFoundError
from borsa.fetchers.base import Fetcher
from borsa.models import (
    BatchQuoteResponse,
    ProviderStats,
    QuoteData,
    SymbolEntry,
    SymbolListResponse,
)
from borsa.services.cache import TTLCacheService

log = structlog.get_logger()


class StocksService:
    def __init__(self, fetchers: list[Fetcher], cache: TTLCacheService) -> None:
        self._fetchers = fetchers
        self._cache = cache
        self._start_time = datetime.utcnow()
        self._stats: dict[str, dict[str, int]] = {
            f.name: {"requests": 0, "successes": 0, "failures": 0} for f in fetchers
        }
        self._bulk_fetch_lock = asyncio.Lock()
        self._bulk_failure_until: dict[str, float] = {}

    # ── Public API ────────────────────────────────────────────────────────────

    async def get_quote(self, symbol: str) -> QuoteData:
        sym = symbol.upper()
        if not is_valid_symbol(sym):
            raise SymbolNotFoundError(sym)
        return await self._cache.get_or_set(f"quote:{sym}", lambda: self._fetch_quote(sym))

    async def get_all_quotes(self) -> list[QuoteData]:
        """Fetch all known EGX symbols in parallel via asyncio.gather."""
        async with self._bulk_fetch_lock:
            return await self._get_all_quotes_unlocked()

    async def refresh_all_quotes(self) -> list[QuoteData]:
        """Force-refresh all known EGX quotes and repopulate the cache."""
        async with self._bulk_fetch_lock:
            self._bulk_failure_until.clear()
            for symbol in EGX_SYMBOLS:
                self._cache.invalidate(f"quote:{symbol}")
            return await self._get_all_quotes_unlocked()

    async def _get_all_quotes_unlocked(self) -> list[QuoteData]:
        now = time.monotonic()
        symbols = [
            symbol for symbol in EGX_SYMBOLS if self._bulk_failure_until.get(symbol, 0) <= now
        ]
        tasks = [
            self._cache.get_or_set(f"quote:{s}", partial(self._fetch_quote, s)) for s in symbols
        ]
        raw = await asyncio.gather(*tasks, return_exceptions=True)
        results: list[QuoteData] = []
        failure_ttl = int(self._cache.stats()["ttl"])
        for symbol, result in zip(symbols, raw, strict=True):
            if isinstance(result, QuoteData):
                results.append(result)
                self._bulk_failure_until.pop(symbol, None)
            else:
                self._bulk_failure_until[symbol] = now + failure_ttl

        skipped = len(EGX_SYMBOLS) - len(symbols)
        log.info(
            "all_quotes_fetched",
            total=len(EGX_SYMBOLS),
            attempted=len(symbols),
            skipped_recent_failures=skipped,
            succeeded=len(results),
        )
        return results

    async def get_batch_quotes(self, symbols: list[str]) -> BatchQuoteResponse:
        valid: list[str] = []
        failed: list[str] = []
        for s in symbols:
            sym = s.upper().strip()
            (valid if is_valid_symbol(sym) else failed).append(sym)

        tasks = [self._cache.get_or_set(f"quote:{s}", partial(self._fetch_quote, s)) for s in valid]
        raw = await asyncio.gather(*tasks, return_exceptions=True)

        results: list[QuoteData] = []
        for sym, r in zip(valid, raw, strict=True):
            if isinstance(r, QuoteData):
                results.append(r)
            else:
                failed.append(sym)

        return BatchQuoteResponse(results=results, failed=failed)

    async def find_by_company(self, name: str) -> QuoteData:
        name_lower = name.lower()
        match = next(
            (sym for sym, meta in EGX_SYMBOLS.items() if name_lower in meta["name"].lower()),
            None,
        )
        if match is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No company found matching '{name}'. "
                f"Try GET /v1/stocks to browse available companies.",
            )
        return await self.get_quote(match)

    def list_symbols(self, sector: str | None = None) -> SymbolListResponse:
        entries = [
            SymbolEntry(
                symbol=sym,
                name=meta["name"],
                sector=meta.get("sector"),
            )
            for sym, meta in EGX_SYMBOLS.items()
            if sector is None or meta.get("sector", "").lower() == sector.lower()
        ]
        return SymbolListResponse(count=len(entries), symbols=entries)

    def provider_status(self) -> dict[str, bool]:
        return {f.name: True for f in self._fetchers}

    def provider_stats(self) -> dict[str, ProviderStats]:
        return {name: ProviderStats(**counts) for name, counts in self._stats.items()}

    def uptime_seconds(self) -> float:
        return (datetime.utcnow() - self._start_time).total_seconds()

    def cache_stats(self) -> dict[str, object]:
        return self._cache.stats()

    # ── Internal ──────────────────────────────────────────────────────────────

    async def _fetch_quote(self, symbol: str) -> QuoteData:
        errors: list[str] = []
        for fetcher in self._fetchers:
            self._stats[fetcher.name]["requests"] += 1
            try:
                result = await fetcher.fetch_quote(symbol)
                if result is not None:
                    self._stats[fetcher.name]["successes"] += 1
                    log.info("quote_fetched", symbol=symbol, provider=fetcher.name)
                    return result
                self._stats[fetcher.name]["failures"] += 1
                errors.append(f"{fetcher.name}: no data returned")
            except Exception as exc:
                self._stats[fetcher.name]["failures"] += 1
                log.warning(
                    "fetcher_exception",
                    provider=fetcher.name,
                    symbol=symbol,
                    error=str(exc),
                )
                errors.append(f"{fetcher.name}: {exc}")

        raise AllFetchersFailed(symbol, errors)
