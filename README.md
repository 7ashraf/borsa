<!-- Badges -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)

# borsa بورصة

Self-hostable FastAPI service for Egyptian Exchange (EGX) market data. borsa ships a broad
EGX symbol catalog and a consistent REST API over user-configured data providers.

> Legal note: borsa is software, not a market-data license. Provider terms, rate limits,
> permitted use, and redistribution rules remain the operator's responsibility. Yahoo
> Finance/yfinance support is disabled by default in `.env.example` because it uses
> unofficial Yahoo access.

## Quickstart

```bash
cp .env.example .env
$EDITOR .env
docker compose up --build
```

The API runs at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/docs`.

## Current API

| Method | Path | Description |
|---|---|---|
| `GET` | `/v1/health` | Service health and configured providers |
| `GET` | `/v1/stocks` | EGX symbol catalog |
| `GET` | `/v1/quote/{symbol}` | One live quote |
| `GET` | `/v1/quotes` | All currently retrievable quotes |
| `GET` | `/v1/quotes/batch?symbols=COMI,ETEL` | Batch quote lookup |
| `GET` | `/v1/quote/by-company/{name}` | Quote lookup by company-name fragment |
| `GET` | `/v1/status` | Provider/cache/status counters |
| `GET` | `/demo/quote/{symbol}` | Optional demo endpoint with global daily limit |

## Provider Posture

- Alpha Vantage and Finnhub require the operator's own keys.
- Yahoo Finance via `yfinance` is an optional, unofficial provider. Enable it only if your use
  complies with Yahoo/yfinance terms.
- Startup quote warmup and scheduled refresh are configurable with `.env`.
- Responses include provider attribution in the response body and `X-Data-Source` header where
  applicable.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `ALPHA_VANTAGE_KEY` | empty | Alpha Vantage key, provider skipped if empty |
| `FINNHUB_KEY` | empty | Finnhub key, provider skipped if empty |
| `ENABLE_YAHOO_FINANCE` | `false` | Enable unofficial Yahoo Finance/yfinance fetching |
| `CACHE_TTL_SECONDS` | `300` | Quote cache TTL and auto-refresh interval |
| `FETCH_QUOTES_ON_STARTUP` | `true` | Fetch all quotes when the app starts |
| `AUTO_REFRESH_QUOTES` | `true` | Force-refresh all quotes every cache TTL |
| `CACHE_MAX_SIZE` | `512` | Maximum cache entries |
| `LOG_LEVEL` | `info` | `debug`, `info`, `warning`, `error` |

## Disclaimer

See [DISCLAIMER.md](DISCLAIMER.md). borsa is not financial, investment, legal, or tax advice.
Data accuracy and availability depend on third-party providers.

## License

MIT © borsa contributors. See [LICENSE](LICENSE).
