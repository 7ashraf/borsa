import pytest

from borsa.services.cache import TTLCacheService


def make_cache() -> TTLCacheService:
    return TTLCacheService(ttl=60, maxsize=128)


async def test_cache_miss_calls_fn() -> None:
    cache = make_cache()
    calls = 0

    async def fn() -> str:
        nonlocal calls
        calls += 1
        return "value"

    result = await cache.get_or_set("k1", fn)
    assert result == "value"
    assert calls == 1


async def test_cache_hit_skips_fn() -> None:
    cache = make_cache()
    calls = 0

    async def fn() -> str:
        nonlocal calls
        calls += 1
        return "value"

    await cache.get_or_set("k2", fn)
    await cache.get_or_set("k2", fn)
    assert calls == 1


async def test_invalidate_removes_entry() -> None:
    cache = make_cache()
    calls = 0

    async def fn() -> str:
        nonlocal calls
        calls += 1
        return "value"

    await cache.get_or_set("k3", fn)
    cache.invalidate("k3")
    await cache.get_or_set("k3", fn)
    assert calls == 2


async def test_stats_includes_hit_rate() -> None:
    cache = make_cache()

    async def fn() -> str:
        return "v"

    await cache.get_or_set("k4", fn)  # miss
    await cache.get_or_set("k4", fn)  # hit

    s = cache.stats()
    assert s["hits"] == 1
    assert s["misses"] == 1
    assert s["hit_rate"] == 0.5


async def test_clear_empties_cache() -> None:
    cache = make_cache()

    async def fn() -> str:
        return "v"

    await cache.get_or_set("k5", fn)
    cache.clear()
    assert cache.stats()["size"] == 0


async def test_two_caches_are_independent() -> None:
    """Two TTLCacheService instances do not share state."""
    c1 = TTLCacheService(ttl=60)
    c2 = TTLCacheService(ttl=600)

    async def fn() -> str:
        return "v"

    await c1.get_or_set("key", fn)
    assert c2.stats()["size"] == 0
