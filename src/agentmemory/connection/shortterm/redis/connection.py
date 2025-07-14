
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
        json.loads("")
        pass

    def set(self, key: str, value: dict) -> None:
        pass

    def clear(self, pattern: str | list[str]) -> None:
        if isinstance(pattern, str):
            pattern = [pattern]
        resp = self._client.delete(*pattern)
        print(resp)
        # TODO...

    def keys(self, pattern: str) -> list[str]:
        pass
