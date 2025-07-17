from abc import ABC, abstractmethod
from typing import Any


class ShorttermMemoryInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> Any | None: pass

    @abstractmethod
    def set(self, key: str, value: Any, ex: int) -> None: pass

    @abstractmethod
    def clear(self, pattern: str | list[str]) -> None: pass

    @abstractmethod
    def keys(self, pattern: str) -> list[str]: pass
