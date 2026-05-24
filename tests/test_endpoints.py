"""FastAPI endpoint smoke tests."""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from borsa.main import app
from borsa.models import ATTRIBUTIONS, BatchQuoteResponse, QuoteData, SymbolListResponse

client = TestClient(app)

_QUOTE = QuoteData(
    symbol="CIBEA",
    company="Commercial International Bank Egypt",
    price=51.0,
    source="Yahoo Finance (COMI.CA)",
    api_symbol="COMI.CA",
    fetch_duration=0.1,
    attribution=ATTRIBUTIONS["yahoo"],
)

_BATCH = BatchQuoteResponse(results=[_QUOTE], failed=[])


# ── Health ────────────────────────────────────────────────────────────────────

def test_health_returns_ok() -> None:
    resp = client.get("/v1/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "version" in body
    assert "providers_configured" in body


# ── Symbols ───────────────────────────────────────────────────────────────────

def test_stocks_list_returns_entries() -> None:
    resp = client.get("/v1/stocks")
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] > 0
    assert len(body["symbols"]) == body["count"]


def test_stocks_filter_by_sector() -> None:
    resp = client.get("/v1/stocks?sector=Financials")
    assert resp.status_code == 200
    body = resp.json()
    for entry in body["symbols"]:
        assert entry["sector"] == "Financials"


# ── Quote ─────────────────────────────────────────────────────────────────────

def test_quote_unknown_symbol_returns_404() -> None:
    resp = client.get("/v1/quote/NOTREAL")
    assert resp.status_code == 404


@patch("borsa.services.stocks.StocksService.get_quote", new_callable=AsyncMock, return_value=_QUOTE)
def test_quote_known_symbol(mock_get: AsyncMock) -> None:
    resp = client.get("/v1/quote/CIBEA")
    assert resp.status_code == 200
    body = resp.json()
    assert body["symbol"] == "CIBEA"
    assert body["price"] == 51.0
    assert "attribution" in body
    assert body["attribution"]["provider"] == "Yahoo Finance"


@patch("borsa.services.stocks.StocksService.get_quote", new_callable=AsyncMock, return_value=_QUOTE)
def test_quote_sets_x_data_source_header(mock_get: AsyncMock) -> None:
    resp = client.get("/v1/quote/CIBEA")
    assert resp.headers.get("x-data-source") == "Yahoo Finance"


def test_request_id_header_present() -> None:
    resp = client.get("/v1/health")
    assert "x-request-id" in resp.headers


def test_request_id_is_echoed_if_provided() -> None:
    resp = client.get("/v1/health", headers={"X-Request-ID": "my-req-123"})
    assert resp.headers.get("x-request-id") == "my-req-123"


# ── All quotes ────────────────────────────────────────────────────────────────

@patch(
    "borsa.services.stocks.StocksService.get_all_quotes",
    new_callable=AsyncMock,
    return_value=[_QUOTE],
)
def test_all_quotes_endpoint(mock_get: AsyncMock) -> None:
    resp = client.get("/v1/quotes")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    assert body[0]["symbol"] == "CIBEA"


# ── Batch quotes ──────────────────────────────────────────────────────────────

@patch(
    "borsa.services.stocks.StocksService.get_batch_quotes",
    new_callable=AsyncMock,
    return_value=_BATCH,
)
def test_batch_quotes_endpoint(mock_get: AsyncMock) -> None:
    resp = client.get("/v1/quotes/batch?symbols=CIBEA,ETEL")
    assert resp.status_code == 200
    body = resp.json()
    assert "results" in body
    assert "failed" in body


# ── Company lookup ────────────────────────────────────────────────────────────

@patch(
    "borsa.services.stocks.StocksService.find_by_company",
    new_callable=AsyncMock,
    return_value=_QUOTE,
)
def test_quote_by_company(mock_get: AsyncMock) -> None:
    resp = client.get("/v1/quote/by-company/telecom")
    assert resp.status_code == 200


# ── Status ────────────────────────────────────────────────────────────────────

def test_status_endpoint() -> None:
    resp = client.get("/v1/status")
    assert resp.status_code == 200
    body = resp.json()
    assert "uptime_seconds" in body
    assert "provider_stats" in body
    assert "cache_stats" in body
    assert "demo_requests_today" in body
