from __future__ import annotations

import time

import httpx
import structlog

from borsa.data.symbols import get_symbol_name, provider_formats
from borsa.models import ATTRIBUTIONS, QuoteData

log = structlog.get_logger()

_BASE = "https://www.alphavantage.co/query"
_ATTRIBUTION = ATTRIBUTIONS["alpha_vantage"]


class AlphaVantageFetcher:
    name = "alpha_vantage"

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    async def fetch_quote(self, symbol: str) -> QuoteData | None:
        start = time.monotonic()
        for fmt in provider_formats(symbol, "alpha_vantage"):
            result = await self._try_format(symbol, fmt, start)
            if result is not None:
                return result
        log.warning("av_all_formats_failed", symbol=symbol)
        return None

    async def _try_format(self, symbol: str, fmt: str, start: float) -> QuoteData | None:
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": fmt,
            "apikey": self._api_key,
        }
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(_BASE, params=params)
            resp.raise_for_status()
            data = resp.json()

            if "Error Message" in data or "Note" in data:
                return None

            quote = data.get("Global Quote", {})
            raw_price = quote.get("05. price")
            if not raw_price or float(raw_price) == 0:
                return None

            price = float(raw_price)
            change_raw = quote.get("09. change")
            pct_raw = quote.get("10. change percent", "")

            return QuoteData(
                symbol=symbol.upper(),
                company=get_symbol_name(symbol) or symbol,
                price=price,
                change=float(change_raw) if change_raw not in (None, "", "N/A") else None,
                change_percent=pct_raw.strip() if pct_raw and pct_raw != "N/A" else None,
                volume=_int_or_none(quote.get("06. volume")),
                high=_float_or_none(quote.get("03. high")),
                low=_float_or_none(quote.get("04. low")),
                source=f"Alpha Vantage ({fmt})",
                api_symbol=fmt,
                fetch_duration=round(time.monotonic() - start, 3),
                attribution=_ATTRIBUTION,
            )
        except Exception as exc:
            log.debug("av_format_failed", fmt=fmt, error=str(exc))
            return None


def _float_or_none(raw: str | None) -> float | None:
    if raw is None or raw in ("", "N/A"):
        return None
    try:
        v = float(raw)
        return v if v != 0 else None
    except ValueError:
        return None


def _int_or_none(raw: str | None) -> int | None:
    if raw is None or raw in ("", "N/A"):
        return None
    try:
        return int(raw)
    except ValueError:
        return None
