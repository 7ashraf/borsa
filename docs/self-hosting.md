---
title: Self-hosting
description: How to run borsa on your own server
---

# Self-hosting

borsa is designed to run anywhere Docker runs — a VPS, a home server, Fly.io, Railway, or any container platform.

## Requirements

- Docker + Docker Compose, **or** Python 3.12+ with `uv`
- At least one provider API key (Yahoo Finance works with no key)

## Docker Compose (recommended)

```bash
git clone https://github.com/your-username/borsa.git
cd borsa
cp .env.example .env
# Edit .env and add your keys
docker compose up -d
```

The service starts on port `8000`. Map a different host port by editing `docker-compose.yml`:

```yaml
ports:
  - "3000:8000"   # host:container
```

## Running with uv

```bash
uv sync
cp .env.example .env
uv run uvicorn borsa.main:app --host 0.0.0.0 --port 8000
```

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `ALPHA_VANTAGE_KEY` | _(empty)_ | Alpha Vantage key, disabled if empty |
| `FINNHUB_KEY` | _(empty)_ | Finnhub key, disabled if empty |
| `ENABLE_YAHOO_FINANCE` | `false` | Enable unofficial Yahoo Finance/yfinance fetching |
| `CACHE_TTL_SECONDS` | `300` | Cache entry lifetime in seconds |
| `DEMO_CACHE_TTL_SECONDS` | `600` | Demo cache entry lifetime in seconds |
| `CACHE_MAX_SIZE` | `512` | Maximum cached entries |
| `FETCH_QUOTES_ON_STARTUP` | `true` | Fetch all `/v1` quotes when the app starts |
| `AUTO_REFRESH_QUOTES` | `true` | Force-refresh all `/v1` quotes every cache TTL |
| `HOST` | `0.0.0.0` | Bind address |
| `PORT` | `8000` | Bind port |
| `LOG_LEVEL` | `info` | `debug` · `info` · `warning` · `error` |

## Reverse proxy (nginx example)

```nginx
server {
    listen 80;
    server_name borsa.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Health check

```bash
curl http://localhost:8000/health
```

Expected: `{"status":"ok", ...}`
