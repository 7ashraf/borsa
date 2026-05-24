---
title: borsa
description: Unified EGX market data API — self-hostable, BYOK
---

# borsa بورصة

Self-hostable FastAPI service for Egyptian Exchange (EGX) market data using operator-configured providers. Yahoo Finance/yfinance support is optional and disabled by default in `.env.example`; review provider terms before enabling it.

## Quickstart

```bash
cp .env.example .env   # add at least one provider key
docker compose up
```

API → `http://localhost:8000`  
Interactive docs → `http://localhost:8000/docs`

## Guides

- [Self-hosting](self-hosting.md)
- [Endpoints reference](endpoints.md)
- [Adding a fetcher](adding-a-fetcher.md)
