from typing import Iterator
from bson import ObjectId

from pymongo.database import Database

from agentmemory.connection.longterm.interface import (
    LongtermMemoryConversationsSchemaInterface,
    LongtermMemoryConversationItemsSchemaInterface
)
from agentmemory.schema.conversations import Conversation, ConversationItem
from agentmemory.utils.dataclasses.default_factory_functions import current_iso_datetime


class MongoDBConversationsSchema(LongtermMemoryConversationsSchemaInterface):
    def __init__(self, db: Database):
        self._col = db["conversations"]

    def get(self, conversation_id: str, cache_cnf: str = None) -> Conversation:
        data = self._col.find_one({"conversation_id": conversation_id})
        if not data:
            raise ValueError(f"Conversation with ID {conversation_id} not found.")
        return Conversation(**data)

    def list(self, query: dict = None, cache_cnf: str = None) -> Iterator[Conversation]:
        query = query or {}
        for data in self._col.find(query).sort("created_at", 1):
            yield Conversation(**data)

    def create(self, conversation: Conversation) -> Conversation:
        conversation._id = ObjectId()
        data = conversation.to_dict()
        res = self._col.insert_one(data)
        conversation._id = str(res.inserted_id)
        return conversation

    def update(self, conversation: Conversation) -> Conversation:
        conversation.updated_at = current_iso_datetime()
        update_data = {
            "title": conversation.title,
            "metadata": conversation.metadata,
            "updated_at": conversation.updated_at
        }

        res = self._col.update_one(
            {"conversation_id": conversation.conversation_id},
            {"$set": update_data}
        )

        if res.modified_count == 0:
            raise ValueError(f"Conversation with ID {conversation.conversation_id} not found or no changes made.")

        return conversation

    def delete(self, conversation_id: str, cascade: bool) -> None:
        # TODO: implement cascade deletion logic if needed -> delete items
        self._col.delete_one({"conversation_id": conversation_id})


class MongoDBConversationItemsSchema(LongtermMemoryConversationItemsSchemaInterface):
    def __init__(self, db: Database):
        self._col = db["conversation_items"]

    def get(self, conversation_id: str, item_id: str, cache_cnf: str = None) -> ConversationItem:
        data = self._col.find_one({"conversation_id": conversation_id, "item_id": item_id})
        if not data:
            raise ValueError(f"Item with ID {item_id} in conversation {conversation_id} not found.")
        return ConversationItem(**data)

    def list(self, conversation_id: str, query: dict = None, cache_cnf: str = None) -> Iterator[ConversationItem]:
        query = query or {}
        query["conversation_id"] = conversation_id
        for data in self._col.find(query).sort("created_at", 1):
            yield ConversationItem(**data)

    def list_until_id_found(self, conversation_id: str, item_id: str, cache_cnf: str = None) -> Iterator[ConversationItem]:
        query = {"conversation_id": conversation_id}
        for data in self._col.find(query).sort("created_at", 1):
            yield ConversationItem(**data)
            if data["item_id"] == item_id:
                break

    def create(self, item: ConversationItem) -> ConversationItem:
        item._id = ObjectId()
        item.created_at = current_iso_datetime()
        item.updated_at = current_iso_datetime()
        data = item.to_dict()
        res = self._col.insert_one(data)
        item._id = str(res.inserted_id)
        return item

    def update(self, item: ConversationItem) -> ConversationItem:
        item.updated_at = current_iso_datetime()
        update_data = {
            "role": item.role,
            "content": item.content,
            "metadata": item.metadata,
            "updated_at": item.updated_at
        }

        res = self._col.update_one(
            {"conversation_id": item.conversation_id, "item_id": item.item_id},
            {"$set": update_data}
        )

        if res.modified_count == 0:
            raise ValueError(f"Item with ID {item.item_id} in conversation {item.conversation_id} not found or no changes made.")

        return item

    def delete(self, item_id: str) -> None:
        self._col.delete_one({"item_id": item_id})
