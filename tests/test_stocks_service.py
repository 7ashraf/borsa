"""Tests for StocksService fallback logic and orchestration."""

from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from borsa.models import ATTRIBUTIONS, QuoteData
from borsa.services.cache import TTLCacheService
from borsa.services.stocks import StocksService

_ATTRIBUTION = ATTRIBUTIONS["yahoo"]

MOCK_QUOTE = QuoteData(
    symbol="CIBEA",
    company="Commercial International Bank Egypt",
    price=51.0,
    source="Yahoo Finance (COMI.CA)",
    api_symbol="COMI.CA",
    fetch_duration=0.1,
    attribution=_ATTRIBUTION,
)


def _make_service(*fetchers: object) -> StocksService:
    cache = TTLCacheService(ttl=60)
    return StocksService(list(fetchers), cache)  # type: ignore[arg-type]


def _mock_fetcher(name: str, result: QuoteData | None) -> AsyncMock:
    f = AsyncMock()
    f.name = name
    f.fetch_quote = AsyncMock(return_value=result)
    return f


async def test_returns_first_successful_provider() -> None:
    av = _mock_fetcher("alpha_vantage", MOCK_QUOTE)
    yahoo = _mock_fetcher("yahoo", MOCK_QUOTE)
    svc = _make_service(av, yahoo)
    result = await svc.get_quote("CIBEA")
    assert result.price == 51.0
    av.fetch_quote.assert_called_once()
    yahoo.fetch_quote.assert_not_called()


async def test_fallback_to_next_provider_when_first_returns_none() -> None:
    av = _mock_fetcher("alpha_vantage", None)
    yahoo = _mock_fetcher("yahoo", MOCK_QUOTE)
    svc = _make_service(av, yahoo)
    result = await svc.get_quote("CIBEA")
    assert result.price == 51.0
    av.fetch_quote.assert_called_once()
    yahoo.fetch_quote.assert_called_once()


async def test_fallback_when_first_raises_exception() -> None:
    av = AsyncMock()
    av.name = "alpha_vantage"
    av.fetch_quote = AsyncMock(side_effect=RuntimeError("network down"))
    yahoo = _mock_fetcher("yahoo", MOCK_QUOTE)
    svc = _make_service(av, yahoo)
    result = await svc.get_quote("CIBEA")
    assert result.price == 51.0


async def test_all_fetchers_fail_raises_503() -> None:
    av = _mock_fetcher("alpha_vantage", None)
    yahoo = _mock_fetcher("yahoo", None)
    svc = _make_service(av, yahoo)
    with pytest.raises(HTTPException) as exc_info:
        await svc.get_quote("CIBEA")
    assert exc_info.value.status_code == 503


async def test_invalid_symbol_raises_404() -> None:
    svc = _make_service(_mock_fetcher("yahoo", MOCK_QUOTE))
    with pytest.raises(HTTPException) as exc_info:
        await svc.get_quote("NOTREAL")
    assert exc_info.value.status_code == 404


async def test_stats_track_successes_and_failures() -> None:
    av = _mock_fetcher("alpha_vantage", None)
    yahoo = _mock_fetcher("yahoo", MOCK_QUOTE)
    svc = _make_service(av, yahoo)
    await svc.get_quote("CIBEA")
    stats = svc.provider_stats()
    assert stats["alpha_vantage"].failures == 1
    assert stats["yahoo"].successes == 1


async def test_get_all_quotes_returns_list() -> None:
    yahoo = _mock_fetcher("yahoo", MOCK_QUOTE)
    svc = _make_service(yahoo)
    results = await svc.get_all_quotes()
    assert isinstance(results, list)
    assert len(results) > 0


async def test_get_batch_quotes_separates_failed() -> None:
    yahoo = _mock_fetcher("yahoo", MOCK_QUOTE)
    svc = _make_service(yahoo)
    resp = await svc.get_batch_quotes(["CIBEA", "ETEL", "NOTREAL"])
    assert "NOTREAL" in resp.failed
    assert len(resp.results) >= 0
