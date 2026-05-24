from __future__ import annotations
import asyncio
import os
import time
from functools import partial
from pathlib import Path
from tempfile import gettempdir

import structlog
import yfinance as yf

from borsa.data.symbols import get_symbol_name, provider_formats
from borsa.models import ATTRIBUTIONS, QuoteData

log = structlog.get_logger()

_ATTRIBUTION = ATTRIBUTIONS["yahoo"]
_YFINANCE_CACHE_DIR = Path(os.getenv("YFINANCE_CACHE_DIR", gettempdir())) / "borsa-yfinance"

try:
    _YFINANCE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    yf.set_tz_cache_location(str(_YFINANCE_CACHE_DIR))
except Exception as exc:
    log.debug("yfinance_cache_setup_failed", error=str(exc))


class YahooFetcher:
    """yfinance wrapper — all blocking I/O is dispatched to a thread pool."""

    name = "yahoo"

    async def fetch_quote(self, symbol: str) -> QuoteData | None:
        start = time.monotonic()
        for fmt in provider_formats(symbol, "yahoo"):
            result = await self._try_format(symbol, fmt, start)
            if result is not None:
                return result
        log.warning("yahoo_all_formats_failed", symbol=symbol)
        return None

    async def _try_format(self, symbol: str, fmt: str, start: float) -> QuoteData | None:
        try:
            hist = await _run_sync(partial(_download, fmt))
            if hist is None or hist.empty:
                return None

            price = float(hist["Close"].iloc[-1])
            if price <= 0:
                return None

            change: float | None = None
            change_pct: str | None = None
            if len(hist) > 1:
                prev = float(hist["Close"].iloc[-2])
                if prev > 0:
                    change = round(price - prev, 4)
                    change_pct = f"{(change / prev * 100):.2f}%"

            volume = (
                int(hist["Volume"].iloc[-1])
                if "Volume" in hist.columns and not hist["Volume"].isna().iloc[-1]
                else None
            )
            high = round(float(hist["High"].iloc[-1]), 4) if "High" in hist.columns else None
            low = round(float(hist["Low"].iloc[-1]), 4) if "Low" in hist.columns else None

            return QuoteData(
                symbol=symbol.upper(),
                company=get_symbol_name(symbol) or symbol,
                price=round(price, 4),
                change=change,
                change_percent=change_pct,
                volume=volume,
                high=high,
                low=low,
                source=f"Yahoo Finance ({fmt})",
                api_symbol=fmt,
                fetch_duration=round(time.monotonic() - start, 3),
                attribution=_ATTRIBUTION,
            )
        except Exception as exc:
            log.debug("yahoo_format_failed", fmt=fmt, error=str(exc))
            return None


async def _run_sync(fn: partial) -> object:  # type: ignore[type-arg]
    return await asyncio.get_event_loop().run_in_executor(None, fn)


def _download(ticker: str) -> object:
    return yf.download(
        ticker,
        period="2d",
        progress=False,
        threads=False,
        timeout=10,
        auto_adjust=False,
        multi_level_index=False,
    )
