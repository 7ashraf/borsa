from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress
from datetime import date
from typing import Annotated

import structlog
import uvicorn
from fastapi import Depends, FastAPI, Path, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from borsa import __version__
from borsa.config import settings
from borsa.exceptions import DemoRateLimitExceeded
from borsa.fetchers.alpha_vantage import AlphaVantageFetcher
from borsa.fetchers.base import Fetcher
from borsa.fetchers.finnhub import FinnhubFetcher
from borsa.fetchers.yahoo import YahooFetcher
from borsa.logging_config import configure_logging
from borsa.middleware import RequestIDMiddleware
from borsa.models import (
    BatchQuoteResponse,
    HealthResponse,
    QuoteData,
    StatusResponse,
    SymbolListResponse,
)
from borsa.services.cache import TTLCacheService
from borsa.services.stocks import StocksService

log = structlog.get_logger()


async def _scheduled_quote_refresh(svc: StocksService, interval_seconds: int) -> None:
    while True:
        await asyncio.sleep(interval_seconds)
        try:
            results = await svc.refresh_all_quotes()
            log.info(
                "scheduled_quotes_refreshed",
                succeeded=len(results),
                interval=interval_seconds,
            )
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            log.warning("scheduled_quotes_refresh_failed", error=str(exc))


async def _warm_quote_cache(svc: StocksService) -> None:
    try:
        results = await svc.get_all_quotes()
        log.info("startup_quotes_refreshed", succeeded=len(results))
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        log.warning("startup_quotes_refresh_failed", error=str(exc))


# ── Rate limiter for /demo ────────────────────────────────────────────────────


class _DemoRateLimiter:
    def __init__(self, daily_limit: int) -> None:
        self._limit = daily_limit
        self._count = 0
        self._reset_date = date.today()

    def check_and_increment(self) -> bool:
        today = date.today()
        if today != self._reset_date:
            self._count = 0
            self._reset_date = today
        if self._count >= self._limit:
            return False
        self._count += 1
        return True

    @property
    def count_today(self) -> int:
        return self._count


# ── Service factory ───────────────────────────────────────────────────────────


def _build_fetchers(av_key: str, fh_key: str, enable_yahoo: bool) -> list[Fetcher]:
    """Build the fetcher chain: Yahoo → AV → Finnhub.

    Providers with no key configured are silently omitted.
    Yahoo Finance needs no key and has the best current EGX coverage.
    """
    fetchers: list[Fetcher] = []
    if enable_yahoo:
        fetchers.append(YahooFetcher())
    if av_key:
        fetchers.append(AlphaVantageFetcher(av_key))
    if fh_key:
        fetchers.append(FinnhubFetcher(fh_key))
    return fetchers


# ── Lifespan ──────────────────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging(settings.log_level, settings.dev_mode)
    log.info("borsa_starting", version=__version__)

    normal_cache = TTLCacheService(ttl=settings.cache_ttl_seconds, maxsize=settings.cache_max_size)
    demo_cache = TTLCacheService(
        ttl=settings.demo_cache_ttl_seconds,
        maxsize=settings.cache_max_size,
    )

    app.state.stock_svc = StocksService(
        _build_fetchers(
            settings.alpha_vantage_key,
            settings.finnhub_key,
            settings.enable_yahoo_finance,
        ),
        normal_cache,
    )
    app.state.demo_svc = StocksService(
        _build_fetchers(
            settings.demo_alpha_vantage_key,
            settings.demo_finnhub_key,
            settings.enable_yahoo_finance,
        ),
        demo_cache,
    )
    app.state.demo_limiter = _DemoRateLimiter(settings.demo_daily_limit)

    log.info(
        "borsa_ready",
        v1_providers=list(app.state.stock_svc.provider_status().keys()),
        demo_providers=list(app.state.demo_svc.provider_status().keys()),
    )

    app.state.quote_refresh_tasks = []
    if settings.fetch_quotes_on_startup:
        app.state.quote_refresh_tasks.append(
            asyncio.create_task(_warm_quote_cache(app.state.stock_svc))
        )
    if settings.auto_refresh_quotes:
        app.state.quote_refresh_tasks.append(
            asyncio.create_task(
                _scheduled_quote_refresh(app.state.stock_svc, settings.cache_ttl_seconds)
            )
        )

    yield

    for task in app.state.quote_refresh_tasks:
        task.cancel()
    for task in app.state.quote_refresh_tasks:
        with suppress(asyncio.CancelledError):
            await task

    log.info("borsa_stopped")


# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="borsa بورصة",
    summary="Unified EGX market data API — self-hostable, BYOK",
    version=__version__,
    license_info={"name": "MIT"},
    lifespan=lifespan,
)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=settings.cors_origin_regex,
    allow_methods=["GET", "DELETE"],
    allow_headers=["*"],
)


# ── Dependency providers ──────────────────────────────────────────────────────


def get_stock_svc(request: Request) -> StocksService:
    return request.app.state.stock_svc  # type: ignore[no-any-return]


def get_demo_svc(request: Request) -> StocksService:
    return request.app.state.demo_svc  # type: ignore[no-any-return]


def get_demo_limiter(request: Request) -> _DemoRateLimiter:
    return request.app.state.demo_limiter  # type: ignore[no-any-return]


StockSvcDep = Annotated[StocksService, Depends(get_stock_svc)]
DemoSvcDep = Annotated[StocksService, Depends(get_demo_svc)]
DemoLimiterDep = Annotated[_DemoRateLimiter, Depends(get_demo_limiter)]


# ── /v1 router ────────────────────────────────────────────────────────────────

from fastapi import APIRouter  # noqa: E402

v1 = APIRouter(prefix="/v1", tags=["v1"])


@v1.get("/health", response_model=HealthResponse)
async def health(svc: StockSvcDep) -> HealthResponse:
    return HealthResponse(
        status="ok",
        version=__version__,
        providers_configured=svc.provider_status(),
    )


@v1.get("/stocks", response_model=SymbolListResponse)
async def list_stocks(
    svc: StockSvcDep,
    sector: Annotated[str | None, Query(description="Filter by sector name")] = None,
) -> SymbolListResponse:
    return svc.list_symbols(sector=sector)


@v1.get("/quote/{symbol}", response_model=QuoteData)
async def get_quote(
    symbol: Annotated[str, Path(description="EGX symbol, e.g. CIBEA")],
    svc: StockSvcDep,
    response: Response,
) -> QuoteData:
    result = await svc.get_quote(symbol)
    response.headers["X-Data-Source"] = result.attribution.provider
    return result


@v1.get("/quotes", response_model=list[QuoteData])
async def get_all_quotes(svc: StockSvcDep, response: Response) -> list[QuoteData]:
    results = await svc.get_all_quotes()
    if results:
        response.headers["X-Data-Source"] = results[0].attribution.provider
    return results


@v1.get("/quotes/batch", response_model=BatchQuoteResponse)
async def get_batch_quotes(
    svc: StockSvcDep,
    symbols: Annotated[str, Query(description="Comma-separated EGX symbols, e.g. CIBEA,ETEL,FWRY")],
) -> BatchQuoteResponse:
    sym_list = [s.strip() for s in symbols.split(",") if s.strip()]
    return await svc.get_batch_quotes(sym_list)


@v1.get("/quote/by-company/{name}", response_model=QuoteData)
async def get_quote_by_company(
    name: Annotated[str, Path(description="Partial company name, e.g. telecom")],
    svc: StockSvcDep,
    response: Response,
) -> QuoteData:
    result = await svc.find_by_company(name)
    response.headers["X-Data-Source"] = result.attribution.provider
    return result


@v1.get("/status", response_model=StatusResponse)
async def status(
    svc: StockSvcDep,
    limiter: DemoLimiterDep,
) -> StatusResponse:
    return StatusResponse(
        uptime_seconds=round(svc.uptime_seconds(), 1),
        total_symbols=len(svc.list_symbols().symbols),
        provider_stats=svc.provider_stats(),
        cache_stats=svc.cache_stats(),
        demo_requests_today=limiter.count_today,
        demo_daily_limit=settings.demo_daily_limit,
    )


app.include_router(v1)


# ── /demo router ──────────────────────────────────────────────────────────────

demo = APIRouter(prefix="/demo", tags=["demo"])


@demo.get(
    "/quote/{symbol}",
    response_model=QuoteData,
    summary="Demo quote — 50 requests/day global limit",
    description=(
        "Uses operator-provided keys. Hard-limited to 50 requests/day across all visitors. "
        "Self-host borsa for unlimited access."
    ),
)
async def demo_quote(
    symbol: Annotated[str, Path(description="EGX symbol")],
    svc: DemoSvcDep,
    limiter: DemoLimiterDep,
    response: Response,
) -> QuoteData:
    if not limiter.check_and_increment():
        raise DemoRateLimitExceeded(settings.demo_daily_limit)
    result = await svc.get_quote(symbol)
    response.headers["X-Data-Source"] = result.attribution.provider
    return result


app.include_router(demo)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run(
        "borsa.main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
        reload=False,
    )
