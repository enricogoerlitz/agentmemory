from typing import Iterator

from agentmemory.schema.conversations import Conversation, ConversationItem
from agentmemory.connection.connection import AgentMemoryConnection
from agentmemory.utils.dataclasses.default_factory_functions import current_iso_datetime
from agentmemory.utils.validation.instance import check_isinstance


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
        check_isinstance(conversation, Conversation)
        return self._con.longterm.conversations().create(conversation)

    def update(self, conversation: Conversation) -> Conversation:
        check_isinstance(conversation, Conversation)
        conversation.updated_at = current_iso_datetime()
        update_data = {
            "title": conversation.title,
            "data": conversation.data,
            "updated_at": conversation.updated_at
        }
        self._con.longterm.conversations().update(
            conversation.conversation_id,
            update_data=update_data
        )
        return conversation

    def delete(self, conversation_id: str, cascade: bool = False) -> None:
        return self._con.longterm.conversations().delete(conversation_id, cascade)

    def _validate_object_instance(conversation) -> None:
        if not isinstance(conversation, Conversation):
            raise ValueError("'conversation' must be an 'Conversation' object.")


class ConversationItems:
    def __init__(self, con: AgentMemoryConnection):
        self._con = con

    def get(self, conversation_id: str, item_id: str, cache_cnf: dict = None) -> ConversationItem:
        return self._con.longterm.conversation_items().get(conversation_id, item_id)

    def list(self, query: dict = None, cache_cnf: dict = None) -> Iterator[ConversationItem]:
        return self._con.longterm.conversation_items().list(query)

    def list_by_conversation_id(self, conversation_id: str, query: dict = None, cache_cnf: dict = None) -> Iterator[ConversationItem]:
        return self._con.longterm.conversation_items().list_by_conversation_id(conversation_id, query)

    def list_until_id_found(self, conversation_id: str, item_id: str, cache_cnf: dict = None) -> Iterator[ConversationItem]:
        return self._con.longterm.conversation_items().list_until_id_found(conversation_id, item_id)

    def create(self, item: ConversationItem) -> ConversationItem:
        check_isinstance(item, ConversationItem)
        return self._con.longterm.conversation_items().create(item)

    def update(self, item: ConversationItem) -> ConversationItem:
        check_isinstance(item, ConversationItem)
        item.updated_at = current_iso_datetime()
        update_data = {
            "role": item.role,
            "content": item.content,
            "data": item.data,
            "updated_at": item.updated_at
        }

        self._con.longterm.conversation_items().update(
            conversation_id=item.conversation_id,
            item_id=item.item_id,
            update_data=update_data
        )
        return item

    def delete(self, conversation_id: str, item_id: str) -> None:
        return self._con.longterm.conversation_items().delete(conversation_id, item_id)
