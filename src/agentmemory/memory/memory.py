from agentmemory.connection.connection import AgentMemoryConnection
from agentmemory.memory.conversations import Conversations, ConversationItems


class AgentMemory:
    def __init__(
            self,
            name: str,
            con: AgentMemoryConnection
    ):
        self._name = name
        self._con = con
        self._conversations = Conversations(con=con)
        self._conversation_items = ConversationItems(con=con)

    @property
    def name(self) -> str:
        return self._name

    @property
    def con(self) -> AgentMemoryConnection:
        return self._con

    @property
    def conversations(self) -> Conversations:
        return self._conversations

    @property
    def conversation_items(self) -> ConversationItems:
        return self._conversation_items
