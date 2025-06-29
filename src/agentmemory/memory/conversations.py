from typing import Iterator

from agentmemory.schema.conversations import Conversation, ConversationItem
from agentmemory.connection.connection import AgentMemoryConnection


# TODO:
# - implement caching for get, list, create, update, delete methods
# - clear cache when conversation is created, updated or deleted

class Conversations:
    def __init__(self, con: AgentMemoryConnection):
        self._con = con

    def get(self, conversation_id: str, cache_cnf: dict = None) -> Conversation:
        return self._con.longterm.conversations().get(conversation_id)

    def list(self, query: dict = None, cache_cnf: dict = None) -> Iterator[Conversation]:
        return self._con.longterm.conversations().list(query)

    def create(self, conversation: Conversation) -> Conversation:
        return self._con.longterm.conversations().create(conversation)

    def update(self, conversation: Conversation) -> Conversation:
        return self._con.longterm.conversations().update(conversation)

    def delete(self, conversation_id: str, cascade: bool = False) -> None:
        return self._con.longterm.conversations().delete(conversation_id, cascade)


class ConversationItems:
    def __init__(self, con: AgentMemoryConnection):
        self._con = con

    def get(self, conversation_id: str, item_id: str, cache_cnf: dict = None) -> ConversationItem:
        return self._con.longterm.conversation_items().get(conversation_id, item_id)

    def list(self, conversation_id: str, query: dict = None, cache_cnf: dict = None) -> Iterator[ConversationItem]:
        return self._con.longterm.conversation_items().list(conversation_id, query)

    def list_until_id_found(self, conversation_id: str, item_id: str, cache_cnf: dict = None) -> Iterator[ConversationItem]:
        return self._con.longterm.conversation_items().list_until_id_found(conversation_id, item_id, cache_cnf)

    def create(self, item: ConversationItem) -> ConversationItem:
        return self._con.longterm.conversation_items().create(item)

    def update(self, item: ConversationItem) -> ConversationItem:
        return self._con.longterm.conversation_items().update(item)

    def delete(self, conversation_id: str, item_id: str) -> None:
        return self._con.longterm.conversation_items().delete(conversation_id, item_id)
