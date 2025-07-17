from typing import Any

from agentmemory.connection.connection import AgentMemoryConnection


class Cache:
    def __init__(self, con: AgentMemoryConnection):
        self._con = con

    def get(self, key: str) -> Any | None:
        if self._con.shortterm is None:
            return None
        return self._con.shortterm.get(key)

    def set(self, key: str, value: dict, ex: int = 60) -> None:
        if self._con.shortterm is None:
            return None
        return self._con.shortterm.set(key, value, ex)

    def clear(self, pattern: str | list[str]) -> None:
        if self._con.shortterm is None:
            return None
        return self._con.shortterm.clear(pattern)

    def keys(self, pattern: str) -> list[str]:
        if self._con.shortterm is None:
            return None
        return self._con.shortterm.keys(pattern)


class AutoCache(Cache):
    def __init__(self, cache: Cache, use_auto_caching: bool):
        self._use_auto_caching = use_auto_caching
        self._cache = cache

    def get(self, key: str) -> Any | None:
        if self._use_auto_caching:
            return self._cache.get(key)
        return None

    def set(self, key: str, value: dict, ex: int = 60) -> None:
        if self._use_auto_caching:
            return self._cache.set(key, value)
        return None

    def clear(self, pattern: str | list[str]) -> None:
        if self._use_auto_caching:
            return self._cache.clear(pattern)
        return None

    def keys(self, pattern: str) -> list[str]:
        if self._use_auto_caching:
            return self._cache.keys(pattern)
        return None
