from enum import Enum


CONVERSATIONS = "conversations"
CONVERSATION_ITEMS = "conversation_items"
WORKFLOWS = "workflows"
WORKFLOW_STEPS = "workflow_steps"
PERSONAS = "personas"


class Collection(str, Enum):
    CONVERSATIONS = CONVERSATIONS
    CONVERSATION_ITEMS = CONVERSATION_ITEMS
    WORKFLOWS = WORKFLOWS
    WORKFLOW_STEPS = WORKFLOW_STEPS

    def members(self) -> list[str]:
        return [member for member in self]
