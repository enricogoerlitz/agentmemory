from pymongo import MongoClient
from mongomock import MongoClient as MongoMockClient

from agentmemory.connection.longterm.interface import (
    LongtermMemoryConnectionInterface
)
from agentmemory.connection.longterm.pymongo.conversations import (
    MongoDBConversationsSchema,
    MongoDBConversationItemsSchema
)
from agentmemory.connection.longterm.pymongo.personas import (
    MongoDBPersonasSchema
)
from agentmemory.connection.longterm.pymongo.workflows import (
    MongoDBWorkflowsSchema,
    MongoDBWorkflowStepsSchema
)


class MongoDBConnection(LongtermMemoryConnectionInterface):
    def __init__(
            self,
            mongo_uri: str,
            database: str,
            is_mock_con: bool = False
    ):
        self._uri = mongo_uri
        self._client = MongoClient(mongo_uri) if not is_mock_con else MongoMockClient()
        self._db = self._client[database]

        self._conversations = MongoDBConversationsSchema(self._db)
        self._conversation_items = MongoDBConversationItemsSchema(self._db)
        self._personas = MongoDBPersonasSchema(self._db)
        self._workflows = MongoDBWorkflowsSchema(self._db)
        self._workflow_steps = MongoDBWorkflowStepsSchema(self._db)

    def conversations(self) -> MongoDBConversationsSchema:
        return self._conversations

    def conversation_items(self) -> MongoDBConversationItemsSchema:
        return self._conversation_items

    def personas(self) -> MongoDBPersonasSchema:
        return self._personas

    def workflows(self) -> MongoDBWorkflowsSchema:
        return self._workflows

    def workflow_steps(self) -> MongoDBWorkflowStepsSchema:
        return self._workflow_steps
