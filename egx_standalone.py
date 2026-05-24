"""
Egyptian Stock Market API — standalone single-file version.
Run: python3 egx_standalone.py
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager, suppress
import uvicorn
import requests
import time
import asyncio
import logging
import os
from datetime import datetime, timedelta
import yfinance as yf
from typing import Dict, List, Optional
from pydantic import BaseModel
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("egx")


# ── Models ────────────────────────────────────────────────────────────────────

class StockData(BaseModel):
    timestamp: str
    symbol: str
    company: str
    price: float
    change: Optional[float] = None
    change_percent: Optional[str] = None
    volume: Optional[int] = None
    high: Optional[float] = None
    low: Optional[float] = None
    currency: str = "EGP"
    source: str
    api_symbol: str
    fetch_duration: float

class StockSummary(BaseModel):
    symbol: str
    company: str
    price: float
    change: Optional[float] = None
    change_percent: Optional[str] = None
    timestamp: str

class SystemStatus(BaseModel):
    total_stocks: int
    last_update: Optional[str] = None
    successful_fetches: int
    failed_fetches: int
    uptime_seconds: float
    next_update_in_seconds: Optional[float] = None


# ── Core API class ────────────────────────────────────────────────────────────

class EgyptianStockAPI:
    ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY", "")
    FINNHUB_KEY = os.getenv("FINNHUB_KEY", "")

    EGYPT_STOCKS = {
        "CIBEA": "Commercial International Bank Egypt",
        "TMGH":  "TMG Holding",
        "ETEL":  "Telecom Egypt",
        "ORAS":  "Orascom Construction PLC",
        "HRHO":  "EFG Holding",
        "BTFH":  "Beltone Financial Holding",
        "EKHO":  "Egyptian Kuwaiti Holding",
        "PHDC":  "Palm Hills Development Company",
        "ORWE":  "Oriental Weavers",
        "ISPH":  "Ibn Sina Pharma",
        "EAST":  "Eastern Company",
        "MFPC":  "Misr Fertilizers Production Company",
        "EMFD":  "Emaar Misr For Development",
        "FWRY":  "Fawry For Banking Technology",
        "JUFO":  "Juhayna Food Industries",
    }

    def __init__(self) -> None:
        self.stocks_data: Dict[str, StockData] = {}
        self.last_update: Optional[str] = None
        self.successful_fetches = 0
        self.failed_fetches = 0
        self.start_time = datetime.now()
        self.is_fetching = False
        self._fetch_lock = threading.Lock()
        self._periodic_update_task: Optional[asyncio.Task] = None

    # ── Provider fetchers ─────────────────────────────────────────────────────

    def _fetch_alpha_vantage(self, symbol: str) -> Optional[dict]:
        if not self.ALPHA_VANTAGE_KEY:
            return None

        stripped = symbol.replace("EA", "")
        for fmt in [symbol, f"{symbol}.EGX", f"{symbol}.CA", f"{symbol}.EG", stripped]:
            try:
                r = requests.get(
                    "https://www.alphavantage.co/query",
                    params={"function": "GLOBAL_QUOTE", "symbol": fmt, "apikey": self.ALPHA_VANTAGE_KEY},
                    timeout=15,
                )
                r.raise_for_status()
                data = r.json()
                if "Error Message" in data or "Note" in data:
                    continue
                q = data.get("Global Quote", {})
                price_str = q.get("05. price", "0")
                if price_str and float(price_str) > 0:
                    return {
                        "price": float(price_str),
                        "change": float(q["09. change"]) if q.get("09. change") not in ("N/A", "", None) else None,
                        "change_percent": q.get("10. change percent"),
                        "volume": int(q["06. volume"]) if q.get("06. volume") not in ("N/A", "", None) else None,
                        "high": float(q["03. high"]) if q.get("03. high") not in ("N/A", "", None) else None,
                        "low": float(q["04. low"]) if q.get("04. low") not in ("N/A", "", None) else None,
                        "source": f"Alpha Vantage ({fmt})",
                        "api_symbol": fmt,
                    }
            except Exception as e:
                log.debug("AV %s error: %s", fmt, e)
        return None

    def _fetch_finnhub(self, symbol: str) -> Optional[dict]:
        if not self.FINNHUB_KEY:
            return None

        stripped = symbol.replace("EA", "")
        for fmt in [symbol, f"{symbol}.EGX", f"EGX:{symbol}", f"{symbol}.CA", stripped]:
            try:
                r = requests.get(
                    "https://finnhub.io/api/v1/quote",
                    params={"symbol": fmt, "token": self.FINNHUB_KEY},
                    timeout=15,
                )
                if r.status_code in (403, 429):
                    continue
                r.raise_for_status()
                d = r.json()
                if d.get("c") and d["c"] != 0:
                    dp = d.get("dp")
                    return {
                        "price": float(d["c"]),
                        "change": float(d["d"]) if d.get("d") else None,
                        "change_percent": f"{dp:.2f}%" if dp else None,
                        "high": float(d["h"]) if d.get("h") else None,
                        "low": float(d["l"]) if d.get("l") else None,
                        "volume": None,
                        "source": f"Finnhub ({fmt})",
                        "api_symbol": fmt,
                    }
            except Exception as e:
                log.debug("Finnhub %s error: %s", fmt, e)
        return None

    def _fetch_yahoo(self, symbol: str) -> Optional[dict]:
        stripped = symbol.replace("EA", "")
        for fmt in [f"{symbol}.CA", f"{symbol}.EG", symbol, f"{symbol}.EGX", f"{stripped}.CA"]:
            try:
                hist = yf.download(fmt, period="2d", progress=False, threads=False,
                                   timeout=10, auto_adjust=False, multi_level_index=False)
                if hist.empty:
                    continue
                price = float(hist["Close"].iloc[-1])
                if price <= 0:
                    continue
                change = change_pct = None
                if len(hist) > 1:
                    prev = float(hist["Close"].iloc[-2])
                    change = round(price - prev, 2)
                    change_pct = f"{(change / prev * 100):.2f}%"
                return {
                    "price": round(price, 2),
                    "change": change,
                    "change_percent": change_pct,
                    "volume": int(hist["Volume"].iloc[-1]) if "Volume" in hist.columns and not hist["Volume"].isna().iloc[-1] else None,
                    "high": round(float(hist["High"].iloc[-1]), 2) if "High" in hist.columns else None,
                    "low": round(float(hist["Low"].iloc[-1]), 2) if "Low" in hist.columns else None,
                    "source": f"Yahoo Finance ({fmt})",
                    "api_symbol": fmt,
                }
            except Exception as e:
                log.debug("Yahoo %s error: %s", fmt, e)
        return None

    # ── Orchestration ─────────────────────────────────────────────────────────

    def fetch_single(self, symbol: str) -> Optional[StockData]:
        company = self.EGYPT_STOCKS.get(symbol)
        if not company:
            return None
        t0 = time.time()
        data = self._fetch_alpha_vantage(symbol)
        if not data:
            data = self._fetch_yahoo(symbol)
        if not data:
            data = self._fetch_finnhub(symbol)
        if data:
            sd = StockData(
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                symbol=symbol, company=company,
                price=data["price"], change=data.get("change"),
                change_percent=data.get("change_percent"),
                volume=data.get("volume"), high=data.get("high"), low=data.get("low"),
                currency="EGP", source=data["source"], api_symbol=data["api_symbol"],
                fetch_duration=round(time.time() - t0, 2),
            )
            log.info("✅ %s (%s): %.2f EGP — %s", company, symbol, data["price"], data["source"])
            return sd
        log.warning("❌ No data for %s (%s)", symbol, company)
        return None

    def fetch_all(self) -> None:
        ok = fail = 0
        with ThreadPoolExecutor(max_workers=5) as ex:
            futures = {ex.submit(self.fetch_single, s): s for s in self.EGYPT_STOCKS}
            for fut in as_completed(futures):
                s = futures[fut]
                try:
                    sd = fut.result()
                    if sd:
                        self.stocks_data[s] = sd
                        ok += 1
                    else:
                        fail += 1
                except Exception as e:
                    log.error("fetch error %s: %s", s, e)
                    fail += 1
        self.successful_fetches, self.failed_fetches = ok, fail
        self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.info("🎯 Done: %d/%d stocks fetched", ok, len(self.EGYPT_STOCKS))

    async def fetch_all_async(self) -> None:
        if not self._fetch_lock.acquire(blocking=False):
            log.warning("Fetch already in progress, skipping")
            return
        self.is_fetching = True
        log.info("🇪🇬 Starting fetch cycle…")
        try:
            await asyncio.to_thread(self.fetch_all)
        except Exception as e:
            log.exception("Fetch cycle failed: %s", e)
        finally:
            self.is_fetching = False
            self._fetch_lock.release()

    async def periodic_updates(self) -> None:
        await self.fetch_all_async()
        while True:
            await asyncio.sleep(3600)
            await self.fetch_all_async()


# ── App setup ─────────────────────────────────────────────────────────────────

api = EgyptianStockAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Egyptian Stock API starting…")
    api._periodic_update_task = asyncio.create_task(api.periodic_updates())
    yield
    if api._periodic_update_task:
        api._periodic_update_task.cancel()
        with suppress(asyncio.CancelledError):
            await api._periodic_update_task


app = FastAPI(
    title="Egyptian Stock Market API",
    description="Real-time EGX data — Alpha Vantage → Yahoo Finance → Finnhub fallback",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "message": "Egyptian Stock Market API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": ["/health", "/status", "/stocks", "/stocks/{symbol}",
                      "/stocks/summary", "/stocks/company/{name}", "/refresh"],
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data_available": len(api.stocks_data) > 0,
        "stocks_loaded": len(api.stocks_data),
    }


@app.get("/status", response_model=SystemStatus)
async def status():
    uptime = (datetime.now() - api.start_time).total_seconds()
    next_in = None
    if api.last_update:
        nxt = datetime.strptime(api.last_update, "%Y-%m-%d %H:%M:%S") + timedelta(hours=1)
        next_in = max(0.0, (nxt - datetime.now()).total_seconds())
    return SystemStatus(
        total_stocks=len(api.EGYPT_STOCKS),
        last_update=api.last_update,
        successful_fetches=api.successful_fetches,
        failed_fetches=api.failed_fetches,
        uptime_seconds=round(uptime, 1),
        next_update_in_seconds=next_in,
    )


@app.get("/stocks", response_model=List[StockData])
async def get_all_stocks():
    if not api.stocks_data:
        raise HTTPException(503, "No data yet — fetch in progress, try again shortly.")
    return list(api.stocks_data.values())


@app.get("/stocks/summary", response_model=List[StockSummary])
async def get_summary():
    if not api.stocks_data:
        raise HTTPException(503, "No data yet.")
    return [
        StockSummary(symbol=s.symbol, company=s.company, price=s.price,
                     change=s.change, change_percent=s.change_percent, timestamp=s.timestamp)
        for s in api.stocks_data.values()
    ]


@app.get("/stocks/company/{name}")
async def get_by_company(name: str):
    match = next((s for s, c in api.EGYPT_STOCKS.items() if name.lower() in c.lower()), None)
    if not match:
        raise HTTPException(404, f"No company matching '{name}'. "
                                 f"Available: {list(api.EGYPT_STOCKS.values())}")
    if match not in api.stocks_data:
        raise HTTPException(503, f"Data for {match} not yet available.")
    return api.stocks_data[match]


@app.get("/stocks/{symbol}", response_model=StockData)
async def get_stock(symbol: str):
    symbol = symbol.upper()
    if symbol not in api.EGYPT_STOCKS:
        raise HTTPException(404, f"'{symbol}' not found. Known: {list(api.EGYPT_STOCKS)}")
    if symbol not in api.stocks_data:
        raise HTTPException(503, f"No data for {symbol} yet.")
    return api.stocks_data[symbol]


@app.post("/refresh")
async def refresh(bg: BackgroundTasks):
    if api.is_fetching:
        return {"status": "in_progress", "message": "Fetch already running"}
    bg.add_task(api.fetch_all_async)
    return {"status": "started", "message": "Refresh initiated"}


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
