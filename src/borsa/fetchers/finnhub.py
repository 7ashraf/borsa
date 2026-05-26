from __future__ import annotations

import time

import httpx
import structlog

from borsa.data.symbols import get_symbol_name, provider_formats
from borsa.models import ATTRIBUTIONS, QuoteData

log = structlog.get_logger()

_BASE = "https://finnhub.io/api/v1"
_ATTRIBUTION = ATTRIBUTIONS["finnhub"]


class FinnhubFetcher:
    name = "finnhub"

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    async def fetch_quote(self, symbol: str) -> QuoteData | None:
        start = time.monotonic()
        for fmt in provider_formats(symbol, "finnhub"):
            result = await self._try_format(symbol, fmt, start)
            if result is not None:
                return result
        log.warning("finnhub_all_formats_failed", symbol=symbol)
        return None

    async def _try_format(self, symbol: str, fmt: str, start: float) -> QuoteData | None:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{_BASE}/quote",
                    params={"symbol": fmt},
                    headers={"X-Finnhub-Token": self._api_key},
                )
            if resp.status_code in (403, 429):
                return None
            resp.raise_for_status()
            d = resp.json()

            price = d.get("c")
            if not price or price == 0:
                return None

            dp = d.get("dp")
            return QuoteData(
                symbol=symbol.upper(),
                company=get_symbol_name(symbol) or symbol,
                price=float(price),
                change=float(d["d"]) if d.get("d") is not None else None,
                change_percent=f"{dp:.2f}%" if dp is not None else None,
                high=float(d["h"]) if d.get("h") else None,
                low=float(d["l"]) if d.get("l") else None,
                volume=None,  # Finnhub quote endpoint does not return volume
                source=f"Finnhub ({fmt})",
                api_symbol=fmt,
                fetch_duration=round(time.monotonic() - start, 3),
                attribution=_ATTRIBUTION,
            )
        except Exception as exc:
            log.debug("finnhub_format_failed", fmt=fmt, error=str(exc))
            return None
