"""Tests for the /demo rate-limit counter."""

from collections.abc import Iterator
from datetime import date, timedelta
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

import borsa.main as main
from borsa.main import _DemoRateLimiter, app
from borsa.models import ATTRIBUTIONS, QuoteData

_QUOTE = QuoteData(
    symbol="ETEL",
    company="Telecom Egypt",
    price=18.5,
    source="Yahoo Finance (ETEL.CA)",
    api_symbol="ETEL.CA",
    fetch_duration=0.1,
    attribution=ATTRIBUTIONS["yahoo"],
)


# ── Unit tests for the limiter itself ─────────────────────────────────────────


def test_limiter_allows_requests_under_limit() -> None:
    limiter = _DemoRateLimiter(daily_limit=3)
    assert limiter.check_and_increment() is True
    assert limiter.check_and_increment() is True
    assert limiter.check_and_increment() is True


def test_limiter_rejects_at_limit() -> None:
    limiter = _DemoRateLimiter(daily_limit=2)
    limiter.check_and_increment()
    limiter.check_and_increment()
    assert limiter.check_and_increment() is False


def test_limiter_resets_on_new_day() -> None:
    limiter = _DemoRateLimiter(daily_limit=1)
    limiter.check_and_increment()
    assert limiter.check_and_increment() is False

    # Simulate date advancing
    tomorrow = date.today() + timedelta(days=1)
    with patch("borsa.main.date") as mock_date:
        mock_date.today.return_value = tomorrow
        assert limiter.check_and_increment() is True


def test_limiter_count_today_property() -> None:
    limiter = _DemoRateLimiter(daily_limit=5)
    limiter.check_and_increment()
    limiter.check_and_increment()
    assert limiter.count_today == 2


# ── Integration tests via TestClient ─────────────────────────────────────────


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setattr(main.settings, "fetch_quotes_on_startup", False)
    monkeypatch.setattr(main.settings, "auto_refresh_quotes", False)
    monkeypatch.setattr(main.settings, "alpha_vantage_key", "")
    monkeypatch.setattr(main.settings, "finnhub_key", "")
    monkeypatch.setattr(main.settings, "demo_alpha_vantage_key", "")
    monkeypatch.setattr(main.settings, "demo_finnhub_key", "")
    monkeypatch.setattr(main.settings, "enable_yahoo_finance", False)
    with TestClient(app) as test_client:
        yield test_client


@patch("borsa.services.stocks.StocksService.get_quote", new_callable=AsyncMock, return_value=_QUOTE)
def test_demo_endpoint_returns_429_when_limit_exceeded(
    mock_get: AsyncMock,
    client: TestClient,
) -> None:
    """Replace the app-level demo limiter with an exhausted one."""
    app.state.demo_limiter = _DemoRateLimiter(daily_limit=0)
    resp = client.get("/demo/quote/ETEL")
    assert resp.status_code == 429
    body = resp.json()
    assert "self-host" in body["detail"].lower()


@patch("borsa.services.stocks.StocksService.get_quote", new_callable=AsyncMock, return_value=_QUOTE)
def test_demo_endpoint_allows_request_under_limit(
    mock_get: AsyncMock,
    client: TestClient,
) -> None:
    app.state.demo_limiter = _DemoRateLimiter(daily_limit=100)
    resp = client.get("/demo/quote/ETEL")
    assert resp.status_code == 200
