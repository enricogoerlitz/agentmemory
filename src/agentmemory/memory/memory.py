from agentmemory.connection.connection import AgentMemoryConnection
from agentmemory.memory.conversations import Conversations, ConversationItems
from agentmemory.memory.personas import Personas
from agentmemory.memory.workflows import Workflows, WorkflowSteps


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
        self._personas = Personas(con=con)
        self._workflows = Workflows(con=con)
        self._workflow_steps = WorkflowSteps(con=con)

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

    @property
    def personas(self) -> Personas:
        return self._personas

    @property
    def workflows(self) -> Workflows:
        return self._workflows

    @property
    def workflow_steps(self) -> WorkflowSteps:
        return self._workflow_steps
