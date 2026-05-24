from __future__ import annotations
import asyncio
from collections.abc import Callable, Coroutine
from typing import Any, TypeVar

import structlog
from cachetools import TTLCache

log = structlog.get_logger()

T = TypeVar("T")


class TTLCacheService:
    """Async-safe TTL cache with hit/miss counters."""

    def __init__(self, ttl: int, maxsize: int = 512) -> None:
        self._cache: TTLCache[str, Any] = TTLCache(maxsize=maxsize, ttl=ttl)
        self._lock = asyncio.Lock()
        self._hits = 0
        self._misses = 0

    async def get_or_set(
        self,
        key: str,
        fn: Callable[[], Coroutine[Any, Any, T]],
    ) -> T:
        async with self._lock:
            if key in self._cache:
                self._hits += 1
                log.debug("cache_hit", key=key)
                return self._cache[key]  # type: ignore[return-value]

        result = await fn()

        async with self._lock:
            self._cache[key] = result
            self._misses += 1
            log.debug("cache_miss_stored", key=key)

        return result

    def invalidate(self, key: str) -> None:
        self._cache.pop(key, None)

    def clear(self) -> None:
        self._cache.clear()

    def stats(self) -> dict[str, Any]:
        total = self._hits + self._misses
        hit_rate = round(self._hits / total, 3) if total else 0.0
        return {
            "size": len(self._cache),
            "maxsize": self._cache.maxsize,
            "ttl": int(self._cache.ttl),
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": hit_rate,
        }
