
import json

from typing import Any
from redis.client import Redis
from agentmemory.connection.shortterm.interface import ShorttermMemoryInterface


class RedisConnection(ShorttermMemoryInterface):
    def __init__(
            self,
            host: str,
            port: str = "6379",
            db: int = 0,
            password: str = None
    ):
        self._client = Redis(
            host=host,
            port=port,
            db=db,
            password=password
        )

    def get(self, key: str) -> Any | None:
        value_str = self._client.get(key)
        if value_str is None:
            return None

        value = json.loads(value_str)
        print("FROM CACHE:", value)
        return value

    def set(self, key: str, value: dict, ex: int) -> None:
        value_str = json.dumps(value)
        return self._client.set(key, value_str, ex=ex)

    def clear(self, pattern: str | list[str]) -> None:
        if isinstance(pattern, str):
            pattern = [pattern]

        patterns = [
            key
            for p in pattern
            for key in self.keys(p)
        ]

        if len(patterns) == 0:
            return None

        print("REMOVE PATTERNS:", patterns)
        self._client.delete(*patterns)

    def keys(self, pattern: str) -> list[str]:
        return self._client.keys(pattern)
