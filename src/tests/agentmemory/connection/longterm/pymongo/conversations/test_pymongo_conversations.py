import pytest

from agentmemory import AgentMemory
from agentmemory.schema.conversations import Conversation, ConversationItem
from agentmemory.exc.errors import ObjectNotFoundError
from agentmemory.utils.dataclasses.default_factory_functions import uuid


def delete_all_conversations(memory: AgentMemory, cascade: bool) -> None:
    for conversation in memory.conversations.list():
        memory.conversations.delete(conversation.conversation_id, cascade=cascade)


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


def test_get_conversation(pymongo_memory: AgentMemory):
    # Prepare
    conv = Conversation(
        title="Test Conversation",
        data={"key": "value"}
    )
    _ = pymongo_memory.conversations.create(conv)

    # Execute
    conv_get = pymongo_memory.conversations.get(conv.conversation_id)

    # Check
    assert conv_get is not None

    assert conv_get._id == conv._id
    assert conv_get.conversation_id == conv.conversation_id
    assert conv_get.title == conv.title
    assert conv_get.data.get("key") == conv.data["key"]
    assert conv_get.created_at == conv.created_at
    assert conv_get.updated_at == conv.updated_at


def test_get_conversation_not_found(pymongo_memory: AgentMemory):
    # Prepare
    not_existing_conversation_id = uuid()

    # Execute & Check
    with pytest.raises(ObjectNotFoundError):
        pymongo_memory.conversations.get(not_existing_conversation_id)


def test_list_conversations(pymongo_memory: AgentMemory):
    # Prepare
    delete_all_conversations(pymongo_memory, True)

    COUNT = 5
    LIMIT_COUNT = 3
    for i in range(0, COUNT):
        pymongo_memory.conversations.create(
            conversation=Conversation(
                title=f"title{i}"
            )
        )

    # Execute
    conversations = pymongo_memory.conversations.list()
    conversations_limit = pymongo_memory.conversations.list(limit=LIMIT_COUNT)
    conversations_query = pymongo_memory.conversations.list(query={"title": "title1"})
    conversations_query_fail = pymongo_memory.conversations.list(query={"title": "titleX"})

    # Check
    assert len(conversations) == COUNT
    assert len(conversations_limit) == LIMIT_COUNT
    assert len(conversations_query) == 1
    assert conversations_query[0].title == "title1"
    assert len(conversations_query_fail) == 0


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

    pymongo_memory.conversations.update(conv)
    conv_updated = pymongo_memory.conversations.get(conv_created.conversation_id)

    # Check
    assert conv_updated is not None

    assert conv_updated.title == conv.title
    assert conv_updated.title != conv_created.title

    assert conv_updated.data.get("key") is None
    assert conv_updated.data.get("keyNew") is not None
    assert conv_updated.data.get("keyNew") == conv.data.get("keyNew")

    assert conv_updated.created_at == conv.created_at
    assert conv_updated.updated_at > conv_updated.created_at


def test_update_conversation_read_only_fields(pymongo_memory: AgentMemory):
    # Prepare
    conv = Conversation(
        title="Test Conversation",
        data={"key": "value"}
    )
    conv_created = pymongo_memory.conversations.create(conv)

    # Execute
    conv.created_at = None

    pymongo_memory.conversations.update(conv)
    conv_updated = pymongo_memory.conversations.get(conv_created.conversation_id)

    # Check
    assert conv_updated is not None

    assert conv_updated.created_at != conv.created_at
    assert conv_updated.created_at == conv_created.created_at


def test_delete_conversation(pymongo_memory: AgentMemory):
    # Prepare
    conv = Conversation(
        title="Test Conversation",
        data={"key": "value"}
    )
    conv_created = pymongo_memory.conversations.create(conv)

    # Execute
    conv_found = pymongo_memory.conversations.get(conv_created.conversation_id)
    pymongo_memory.conversations.delete(conv_created.conversation_id)

    # Check
    assert conv_found is not None

    with pytest.raises(ObjectNotFoundError):
        pymongo_memory.conversations.get(conv_created.conversation_id)


def test_delete_conversation_cascade(pymongo_memory: AgentMemory):
    # Prepare
    conv_1 = Conversation(
        title="Test Conversation",
        data={"key": "value"}
    )
    conv_2 = Conversation(
        title="Test Conversation 2"
    )
    conv_created_1 = pymongo_memory.conversations.create(conv_1)
    conv_created_2 = pymongo_memory.conversations.create(conv_2)

    ITEM_COUNT = 3

    for i in range(0, ITEM_COUNT):
        pymongo_memory.conversation_items.create(
            item=ConversationItem(
                conversation_id=conv_created_1.conversation_id,
                role=f"role{i}-1",
                content=f"content-{i}-1"
            )
        )
        pymongo_memory.conversation_items.create(
            item=ConversationItem(
                conversation_id=conv_created_2.conversation_id,
                role=f"role{i}-2",
                content=f"content-{i}-2"
            )
        )

    # Execute
    pymongo_memory.conversations.delete(conv_created_1.conversation_id, cascade=True)
    pymongo_memory.conversations.delete(conv_created_2.conversation_id, cascade=False)
    items_1 = pymongo_memory.conversation_items.list_by_conversation_id(conv_created_1.conversation_id)
    items_2 = pymongo_memory.conversation_items.list_by_conversation_id(conv_created_2.conversation_id)

    # Check
    assert len(items_1) == 0
    assert len(items_2) == ITEM_COUNT
