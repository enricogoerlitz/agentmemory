from pymongo import MongoClient

from agentmemory.connection.longterm.interface import (
    LongtermMemoryConnectionInterface
)
from agentmemory.connection.longterm.pymongo.conversations import (
    MongoDBConversationsSchema,
    MongoDBConversationItemsSchema
)


class MongoDBConnection(LongtermMemoryConnectionInterface):
    def __init__(self, mongo_uri: str, database: str):
        self._uri = mongo_uri
        self._client = MongoClient(mongo_uri)
        self._db = self._client[database]

        self._conversations = MongoDBConversationsSchema(self._db)
        self._conversation_items = MongoDBConversationItemsSchema(self._db)

    def conversations(self) -> MongoDBConversationsSchema:
        return self._conversations

    def conversation_items(self) -> MongoDBConversationItemsSchema:
        return self._conversation_items
