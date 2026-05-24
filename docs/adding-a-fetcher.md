---
title: Adding a fetcher
description: How to add a new data provider to borsa
---

# Adding a new fetcher

See the [Contributing guide](../CONTRIBUTING.md#how-to-add-a-new-fetcher) for the full walkthrough. This page summarises the steps.

## Steps

1. **Create** `src/borsa/fetchers/my_provider.py` — implement `name`, `enabled`, `get_quote`, `get_historical`, `get_company_info`
2. **Add config** — `my_provider_api_key` and `enable_my_provider` in `src/borsa/config.py`
3. **Document env vars** — add entries to `.env.example`
4. **Register** — import in `src/borsa/fetchers/__init__.py` and add an instance to `_fetchers` in `src/borsa/services/stocks.py`
5. **Test** — create `tests/test_fetcher_my_provider.py` using `pytest-httpx` to mock HTTP calls
6. **Update README** — add the new env vars to the table

## Fetcher contract

```python
class MyFetcher:
    name = "my_provider"

    @property
    def enabled(self) -> bool: ...

    async def get_quote(self, symbol: str, yahoo_ticker: str) -> Quote: ...
    async def get_historical(self, symbol, yahoo_ticker, interval, period) -> HistoricalData: ...
    async def get_company_info(self, symbol: str, yahoo_ticker: str) -> CompanyInfo: ...
```

Raise `borsa.exceptions.FetcherError` on any failure — never let raw exceptions escape.
Use `httpx.AsyncClient` for all HTTP calls.
