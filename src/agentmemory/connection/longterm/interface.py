from abc import ABC, abstractmethod
from typing import Iterator

from agentmemory.schema.conversations import Conversation, ConversationItem


class LongtermMemoryConversationsSchemaInterface(ABC):
    @abstractmethod
    def get(self, conversation_id: str, cache_cnf: str = None) -> Conversation: pass

    @abstractmethod
    def list(self, query: dict = None, cache_cnf: str = None) -> Iterator[Conversation]: pass

    @abstractmethod
    def create(self, conversation_id: str, title: str, metadata: dict) -> Conversation: pass

    @abstractmethod
    def update(self, conversation_id: str, title: str = None, metadata: dict = None) -> Conversation: pass

    @abstractmethod
    def delete(self, conversation_id: str, cascade: bool) -> None: pass


class LongtermMemoryConversationItemsSchemaInterface(ABC):
    @abstractmethod
    def get(self, conversation_id: str, item_id: str, cache_cnf: str = None) -> ConversationItem: pass

    @abstractmethod
    def list(self, conversation_id: str, query: dict = None, cache_cnf: str = None) -> Iterator[ConversationItem]: pass

    @abstractmethod
    def list_until_id_found(self, conversation_id: str, item_id: str, cache_cnf: str = None) -> Iterator[ConversationItem]: pass

    @abstractmethod
    def create(self, item: ConversationItem) -> ConversationItem: pass

    @abstractmethod
    def update(self, item: ConversationItem) -> ConversationItem: pass

    @abstractmethod
    def delete(self, conversation_id: str, item_id: str) -> None: pass


class LongtermMemoryConnectionInterface(ABC):
    @abstractmethod
    def conversations(self) -> LongtermMemoryConversationsSchemaInterface: pass

    @abstractmethod
    def conversation_items(self) -> LongtermMemoryConversationItemsSchemaInterface: pass
