# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of borsa — unified EGX market data API
- BYOK architecture for Alpha Vantage, Finnhub, and Yahoo Finance
- `/quotes/{symbol}` — real-time quote with provider fallback
- `/historical/{symbol}` — OHLCV history (daily / weekly / monthly)
- `/company/{symbol}` — company fundamentals
- `/symbols` — searchable EGX symbol dictionary with sector filter
- In-process TTL cache via `cachetools`
- `pydantic-settings` environment-variable configuration
- Dockerfile (python:3.12-slim, uv, non-root user)
- GitHub Actions CI for lint, type-check, and tests
- `justfile` developer shortcuts

[Unreleased]: https://github.com/your-username/borsa/compare/HEAD...HEAD
