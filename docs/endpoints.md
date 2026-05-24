---
title: Endpoints
description: Full API reference for borsa
---

# Endpoints

Base URL: `http://localhost:8000` or your self-hosted domain.

## GET /v1/health

Returns service status and configured providers.

```json
{
  "status": "ok",
  "version": "0.1.0",
  "providers_configured": {
    "yahoo": true,
    "alpha_vantage": true,
    "finnhub": true
  }
}
```

## GET /v1/stocks

Returns the EGX symbol catalog. This endpoint does not fetch prices.

```json
{
  "count": 223,
  "symbols": [
    {
      "symbol": "COMI",
      "name": "Commercial International Bank Egypt (CIB) S.A.E.",
      "sector": "Financials"
    }
  ]
}
```

## GET /v1/quote/{symbol}

Returns one current quote.

```json
{
  "symbol": "COMI",
  "company": "Commercial International Bank Egypt (CIB) S.A.E.",
  "price": 131.5,
  "change": null,
  "change_percent": null,
  "volume": 1727840,
  "high": 132.96,
  "low": 131.5,
  "currency": "EGP",
  "source": "Yahoo Finance (COMI.CA)",
  "api_symbol": "COMI.CA",
  "fetch_duration": 1.443,
  "timestamp": "2026-05-24T20:06:19.388231",
  "attribution": {
    "provider": "Yahoo Finance",
    "url": "https://finance.yahoo.com"
  }
}
```

## GET /v1/quotes

Returns all quotes currently retrievable from configured providers. Symbols with no provider data are
omitted from the response.

## GET /v1/quotes/batch

Query parameter: `symbols`, a comma-separated symbol list.

Example: `/v1/quotes/batch?symbols=COMI,ETEL,FWRY`

```json
{
  "results": [],
  "failed": []
}
```

## GET /v1/quote/by-company/{name}

Finds the first company whose name contains the path fragment, then returns its quote.

## GET /v1/status

Returns current service counters.

```json
{
  "uptime_seconds": 58.9,
  "total_symbols": 223,
  "provider_stats": {},
  "cache_stats": {
    "size": 200,
    "maxsize": 512,
    "ttl": 300,
    "hits": 200,
    "misses": 200,
    "hit_rate": 0.5
  },
  "demo_requests_today": 0,
  "demo_daily_limit": 50
}
```

## GET /demo/quote/{symbol}

Optional demo quote endpoint with a global daily request limit.
