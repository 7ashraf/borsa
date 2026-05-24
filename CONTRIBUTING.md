# Contributing to borsa

Thank you for helping improve EGX data tooling for everyone. This document covers everything you need to go from zero to open PR.

---

## Table of contents

1. [Dev setup](#dev-setup)
2. [Running tests, lint, and type checks](#running-tests-lint-and-type-checks)
3. [Commit message convention](#commit-message-convention)
4. [PR process](#pr-process)
5. [What makes a good first issue](#what-makes-a-good-first-issue)
6. [How to add a new fetcher](#how-to-add-a-new-fetcher)

---

## Dev setup

**Prerequisites:** Python 3.12+, [uv](https://github.com/astral-sh/uv), [just](https://github.com/casey/just) (optional but handy).

```bash
git clone https://github.com/your-username/borsa.git
cd borsa

# Install all dependencies including dev extras
uv sync --extra dev

# Copy the env template (no real keys needed for tests)
cp .env.example .env

# Install pre-commit hooks
uv run pre-commit install
```

The project uses `src/` layout. The package is `borsa`; import it as `from borsa.xxx import yyy`.

---

## Running tests, lint, and type checks

```bash
# Run the full test suite
just test
# or: uv run pytest -v

# Lint with ruff
just lint
# or: uv run ruff check src tests

# Auto-format
just fmt
# or: uv run ruff format src tests

# Static type checking
just typecheck
# or: uv run mypy src

# Everything at once (mirrors CI)
just check
```

All three must pass before opening a PR. CI enforces the same checks.

---

## Commit message convention

borsa follows **Conventional Commits** (`type(scope): description`):

| Type | When to use |
|------|-------------|
| `feat` | New user-facing feature |
| `fix` | Bug fix |
| `refactor` | Code change that is neither a fix nor a feature |
| `test` | Adding or updating tests |
| `docs` | Documentation only |
| `chore` | Build, CI, dependency updates |
| `perf` | Performance improvement |

**Examples:**

```
feat(fetchers): add MSCI fetcher for emerging market data
fix(yahoo): handle missing regularMarketPrice field
docs(readme): add mermaid architecture diagram
chore(ci): pin uv to v0.4
```

Rules:
- Lowercase type and description
- Present tense ("add" not "added")
- No period at the end
- Body lines ≤ 72 characters
- Reference issues with `Closes #123` in the commit body (not the subject)

---

## PR process

1. **Branch from `main`:** `git checkout -b feat/your-feature-name`
2. **Keep PRs focused** — one logical change per PR makes review faster.
3. **Write tests** — new behaviour needs test coverage; bug fixes should include a regression test.
4. **CI must pass** — lint, type check, and tests all green before requesting review.
5. **Update CHANGELOG.md** — add a line under `[Unreleased]` for any user-facing change.
6. **Fill in the PR template** — especially the summary and checklist.
7. **Request review** — a maintainer will respond within a few days.

For large or uncertain changes, open an issue first to discuss the approach before writing code.

---

## What makes a good first issue

Look for issues labelled **`good first issue`**. These are typically:

- Adding a missing EGX symbol to `src/borsa/data/symbols.py`
- Improving error messages or log output
- Adding a test for an untested code path
- Documentation fixes or additions
- Bumping a dependency

If you find a missing symbol or a data accuracy issue, a PR adding the fix is always welcome — no issue needed first.

---

## How to add a new fetcher

Adding a third-party data provider is the most common contribution. Here is the exact recipe:

### 1. Create the fetcher module

```
src/borsa/fetchers/my_provider.py
```

Your class must satisfy the `Fetcher` protocol defined in `src/borsa/fetchers/base.py`:

```python
from borsa.fetchers.base import Fetcher  # Protocol — for reference only

class MyProviderFetcher:
    name = "my_provider"           # unique snake_case string

    @property
    def enabled(self) -> bool:
        # Return True only when the key is set AND the feature flag is on
        return bool(settings.my_provider_api_key) and settings.enable_my_provider

    async def get_quote(self, symbol: str, yahoo_ticker: str) -> Quote: ...
    async def get_historical(self, symbol, yahoo_ticker, interval, period) -> HistoricalData: ...
    async def get_company_info(self, symbol: str, yahoo_ticker: str) -> CompanyInfo: ...
```

Use `httpx.AsyncClient` for all HTTP calls — no `requests`, no `aiohttp`.  
Raise `borsa.exceptions.FetcherError` on any data or HTTP problem so the orchestrator can fall back gracefully.

### 2. Add config fields

In `src/borsa/config.py`:

```python
my_provider_api_key: str = ""
enable_my_provider: bool = True
```

### 3. Document the env vars

Add the new variables to `.env.example` with a comment explaining where to get a key.

### 4. Register the fetcher

In `src/borsa/fetchers/__init__.py`, import and export your class.

In `src/borsa/services/stocks.py`, add an instance to `_fetchers`:

```python
from borsa.fetchers.my_provider import MyProviderFetcher

_fetchers: list[Fetcher] = [
    AlphaVantageFetcher(),
    FinnhubFetcher(),
    MyProviderFetcher(),   # ← add here; position = fallback priority
    YahooFetcher(),
]
```

### 5. Write tests

Create `tests/test_fetcher_my_provider.py`. Mock HTTP calls with `pytest-httpx`. Verify both the happy path and `FetcherError` on bad responses.

### 6. Update docs

Add a row to the "Self-hosting → Environment variables" table in `README.md`.
