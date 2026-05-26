from __future__ import annotations

from typing import Protocol, runtime_checkable

from borsa.models import QuoteData


@runtime_checkable
class Fetcher(Protocol):
    """Contract every data-provider adapter must satisfy.

    Fetchers receive their API key via constructor injection and never read
    from environment variables directly. Returning None signals "no data
    available" so the orchestrator can try the next provider.
    """

    name: str

    async def fetch_quote(self, symbol: str) -> QuoteData | None: ...
