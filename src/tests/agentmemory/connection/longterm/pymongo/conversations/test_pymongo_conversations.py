import time

from agentmemory import AgentMemory
from agentmemory.schema.conversations import Conversation


def test_create_conversation(pymongo_memory: AgentMemory):
    # Prepare
    conv = Conversation(
        title="Test Conversation",
        data={"key": "value"}
    )

    # Execute
    conv_created = pymongo_memory.conversations.create(conv)

    # Check
    assert conv_created is not None

    assert conv_created._id is not None
    assert conv_created.conversation_id is not None
    assert conv_created.created_at is not None
    assert conv_created.updated_at is not None

    assert conv_created._id == conv._id
    assert conv_created.conversation_id == conv.conversation_id
    assert conv_created.title == conv.title
    assert conv_created.data.get("key") == conv.data["key"]
    assert conv_created.created_at == conv.created_at
    assert conv_created.updated_at == conv.updated_at


def test_update_conversation(pymongo_memory: AgentMemory):
    # Prepare
    conv = Conversation(
        title="Test Conversation",
        data={"key": "value"}
    )
    conv_created = pymongo_memory.conversations.create(conv)

    # Execute
    conv.title = "New title"
    conv.data = {"keyNew": "valueNew"}

    time.sleep(1)
    conv_updated = pymongo_memory.conversations.update(conv)

    # Check
    assert conv_updated is not None

    assert conv_updated.title == conv.title
    assert conv_updated != conv_created.title

    assert conv_updated.data.get("key") is None
    assert conv_updated.data.get("keyNew") is not None
    assert conv_updated.data.get("keyNew") == conv.data.get("keyNew")

    assert conv_updated.created_at == conv.created_at
    assert conv_updated.updated_at > conv_updated.created_at
