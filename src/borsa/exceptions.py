from __future__ import annotations
from fastapi import HTTPException, status


class SymbolNotFoundError(HTTPException):
    def __init__(self, symbol: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Symbol '{symbol}' not found in EGX symbol list.",
        )


class AllFetchersFailed(HTTPException):
    def __init__(self, symbol: str, errors: list[str]) -> None:
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "message": f"All data providers failed for symbol '{symbol}'.",
                "errors": errors,
            },
        )


class DemoRateLimitExceeded(HTTPException):
    def __init__(self, limit: int) -> None:
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=(
                f"The demo endpoint has reached its daily limit of {limit} requests. "
                "Self-host borsa with your own keys for unlimited access — "
                "see the README for a 60-second docker compose setup."
            ),
        )
