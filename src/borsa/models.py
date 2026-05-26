from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Attribution(BaseModel):
    provider: str
    url: str


ATTRIBUTIONS: dict[str, Attribution] = {
    "alpha_vantage": Attribution(provider="Alpha Vantage", url="https://www.alphavantage.co"),
    "finnhub": Attribution(provider="Finnhub", url="https://finnhub.io"),
    "yahoo": Attribution(provider="Yahoo Finance", url="https://finance.yahoo.com"),
}


class QuoteData(BaseModel):
    symbol: str
    company: str
    price: float
    change: float | None = None
    change_percent: str | None = None
    volume: int | None = None
    high: float | None = None
    low: float | None = None
    currency: str = "EGP"
    source: str  # e.g. "Alpha Vantage (CIBEA.EGX)"
    api_symbol: str  # the ticker format that actually returned data
    fetch_duration: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    attribution: Attribution


class SymbolEntry(BaseModel):
    symbol: str
    name: str
    sector: str | None = None


class SymbolListResponse(BaseModel):
    count: int
    symbols: list[SymbolEntry]


class BatchQuoteResponse(BaseModel):
    results: list[QuoteData]
    failed: list[str]


class ProviderStats(BaseModel):
    requests: int
    successes: int
    failures: int


class StatusResponse(BaseModel):
    uptime_seconds: float
    total_symbols: int
    provider_stats: dict[str, ProviderStats]
    cache_stats: dict[str, Any]
    demo_requests_today: int
    demo_daily_limit: int


class HealthResponse(BaseModel):
    status: str
    version: str
    providers_configured: dict[str, bool]
