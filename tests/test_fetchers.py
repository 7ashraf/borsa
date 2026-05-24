"""Per-fetcher unit tests using respx to mock httpx calls."""

import json

import httpx
import pytest
import respx

from borsa.fetchers.alpha_vantage import AlphaVantageFetcher
from borsa.fetchers.finnhub import FinnhubFetcher
from borsa.models import QuoteData

# ── Alpha Vantage ─────────────────────────────────────────────────────────────

AV_SUCCESS = {
    "Global Quote": {
        "01. symbol": "CIBEA",
        "02. open": "50.00",
        "03. high": "51.50",
        "04. low": "49.50",
        "05. price": "51.00",
        "06. volume": "1000000",
        "09. change": "1.00",
        "10. change percent": "2.00%",
    }
}

AV_EMPTY = {"Global Quote": {}}


@respx.mock
async def test_alpha_vantage_returns_quote_on_success() -> None:
    respx.get("https://www.alphavantage.co/query").mock(
        return_value=httpx.Response(200, json=AV_SUCCESS)
    )
    fetcher = AlphaVantageFetcher(api_key="testkey")
    result = await fetcher.fetch_quote("CIBEA")
    assert isinstance(result, QuoteData)
    assert result.price == 51.0
    assert result.symbol == "CIBEA"
    assert result.attribution.provider == "Alpha Vantage"


@respx.mock
async def test_alpha_vantage_returns_none_on_empty_response() -> None:
    respx.get("https://www.alphavantage.co/query").mock(
        return_value=httpx.Response(200, json=AV_EMPTY)
    )
    fetcher = AlphaVantageFetcher(api_key="testkey")
    result = await fetcher.fetch_quote("CIBEA")
    assert result is None


@respx.mock
async def test_alpha_vantage_returns_none_on_error_message() -> None:
    respx.get("https://www.alphavantage.co/query").mock(
        return_value=httpx.Response(200, json={"Error Message": "Invalid API call."})
    )
    fetcher = AlphaVantageFetcher(api_key="testkey")
    result = await fetcher.fetch_quote("CIBEA")
    assert result is None


@respx.mock
async def test_alpha_vantage_returns_none_on_http_error() -> None:
    respx.get("https://www.alphavantage.co/query").mock(
        return_value=httpx.Response(500)
    )
    fetcher = AlphaVantageFetcher(api_key="testkey")
    result = await fetcher.fetch_quote("CIBEA")
    assert result is None


# ── Finnhub ───────────────────────────────────────────────────────────────────

FH_SUCCESS = {"c": 51.0, "d": 1.0, "dp": 2.0, "h": 51.5, "l": 49.5, "o": 50.0, "pc": 50.0}
FH_ZERO = {"c": 0, "d": 0, "dp": 0}


@respx.mock
async def test_finnhub_returns_quote_on_success() -> None:
    respx.get("https://finnhub.io/api/v1/quote").mock(
        return_value=httpx.Response(200, json=FH_SUCCESS)
    )
    fetcher = FinnhubFetcher(api_key="testkey")
    result = await fetcher.fetch_quote("CIBEA")
    assert isinstance(result, QuoteData)
    assert result.price == 51.0
    assert result.attribution.provider == "Finnhub"


@respx.mock
async def test_finnhub_returns_none_on_zero_price() -> None:
    respx.get("https://finnhub.io/api/v1/quote").mock(
        return_value=httpx.Response(200, json=FH_ZERO)
    )
    fetcher = FinnhubFetcher(api_key="testkey")
    result = await fetcher.fetch_quote("CIBEA")
    assert result is None


@respx.mock
async def test_finnhub_returns_none_on_403() -> None:
    respx.get("https://finnhub.io/api/v1/quote").mock(
        return_value=httpx.Response(403)
    )
    fetcher = FinnhubFetcher(api_key="testkey")
    result = await fetcher.fetch_quote("CIBEA")
    assert result is None


@respx.mock
async def test_finnhub_change_percent_formatted() -> None:
    respx.get("https://finnhub.io/api/v1/quote").mock(
        return_value=httpx.Response(200, json=FH_SUCCESS)
    )
    fetcher = FinnhubFetcher(api_key="testkey")
    result = await fetcher.fetch_quote("CIBEA")
    assert result is not None
    assert result.change_percent == "2.00%"
