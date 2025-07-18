import pytest

from agentmemory import AgentMemory
from agentmemory.schema.conversations import ConversationItem
from agentmemory.exc.errors import ObjectNotFoundError
from agentmemory.utils.dataclasses.default_factory_functions import uuid


def delete_all_conversation_items(memory: AgentMemory, cascade: bool) -> None:
    for item in memory.conversation_items.list():
        memory.conversation_items.delete(item.conversation_id, item.item_id)


def test_create_conversation_item(pymongo_memory: AgentMemory):
    # Prepare
    item = ConversationItem(
        conversation_id=uuid(),
        role="role",
        content="content",
        data={"key": "value"}
    )

    # Execute
    item_created = pymongo_memory.conversation_items.create(item)

    # Check
    assert item_created is not None

    assert item_created._id is not None
    assert item_created.conversation_id is not None
    assert item_created.created_at is not None
    assert item_created.updated_at is not None

    assert item_created._id == item._id
    assert item_created.conversation_id == item.conversation_id
    assert item_created.role == item.role
    assert item_created.content == item.content
    assert item_created.data.get("key") == item.data["key"]
    assert item_created.created_at == item.created_at
    assert item_created.updated_at == item.updated_at


def test_get_conversation_item(pymongo_memory: AgentMemory):
    # Prepare
    item = ConversationItem(
        conversation_id=uuid(),
        role="role",
        content="content",
        data={"key": "value"}
    )
    _ = pymongo_memory.conversation_items.create(item)

    # Execute
    item_get = pymongo_memory.conversation_items.get(item.conversation_id, item.item_id)

    # Check
    assert item_get is not None

    assert item_get._id == item._id
    assert item_get.conversation_id == item.conversation_id
    assert item_get.role == item.role
    assert item_get.content == item.content
    assert item_get.data.get("key") == item.data["key"]
    assert item_get.created_at == item.created_at
    assert item_get.updated_at == item.updated_at


def test_get_conversation_item_not_found(pymongo_memory: AgentMemory):
    # Prepare
    not_existing_conversation_id = uuid()
    not_existing_conversation_item_id = uuid()

    # Execute & Check
    with pytest.raises(ObjectNotFoundError):
        pymongo_memory.conversation_items.get(
            not_existing_conversation_id,
            not_existing_conversation_item_id
        )


def test_list_conversation_items(pymongo_memory: AgentMemory):
    # Prepare
    delete_all_conversation_items(pymongo_memory, True)

    CONV_ID = uuid()

    COUNT = 5
    LIMIT_COUNT = 3
    for i in range(0, COUNT):
        pymongo_memory.conversation_items.create(
            item=ConversationItem(
                conversation_id=CONV_ID,
                role="role",
                content=f"content-{i}",
                data={"key": "value"}
            )
        )

    # Execute
    items = pymongo_memory.conversation_items.list()
    items_limit = pymongo_memory.conversation_items.list(limit=LIMIT_COUNT)
    items_query = pymongo_memory.conversation_items.list(query={"content": "content-1"})
    items_query_fail = pymongo_memory.conversation_items.list(query={"content": "content-X"})

    pymongo_memory.conversation_items.list_by_conversation_id
    pymongo_memory.conversation_items.list_until_id_found
    # Check
    assert len(items) == COUNT
    assert len(items_limit) == LIMIT_COUNT
    assert len(items_query) == 1
    assert items_query[0].content == "content-1"
    assert len(items_query_fail) == 0


def test_list_conversation_items_by_conversation_id(pymongo_memory: AgentMemory):
    # Prepare
    delete_all_conversation_items(pymongo_memory, True)

    conv_id_1 = uuid()
    conv_id_2 = uuid()

    COUNT = 5
    LIMIT_COUNT = 3
    for conv_id in [conv_id_1, conv_id_2]:
        for i in range(0, COUNT):
            pymongo_memory.conversation_items.create(
                item=ConversationItem(
                    conversation_id=conv_id,
                    role="role",
                    content=f"content-{i}",
                    data={"key": "value"}
                )
            )

    pymongo_memory.conversation_items.create(
        item=ConversationItem(
            conversation_id=conv_id,
            role="role",
            content="content-1",
            data={"key": "value"}
        )
    )

    # Execute
    conv_items_1 = pymongo_memory.conversation_items.list_by_conversation_id(conv_id_1)
    conv_items_2 = pymongo_memory.conversation_items.list_by_conversation_id(conv_id_2)
    conv_items_limit = pymongo_memory.conversation_items.list_by_conversation_id(conv_id_1, limit=LIMIT_COUNT)
    conv_items_query_1 = pymongo_memory.conversation_items.list_by_conversation_id(conv_id_1, query={"content": "content-1"})
    conv_items_query_2 = pymongo_memory.conversation_items.list_by_conversation_id(conv_id_2, query={"content": "content-1"})
    conv_items_query_fail = pymongo_memory.conversation_items.list_by_conversation_id(conv_id_1, query={"content": "XXX"})

    # Check
    assert len(conv_items_1) == COUNT
    assert len(conv_items_2) == COUNT + 1

    assert len(conv_items_limit) == LIMIT_COUNT

    assert len(conv_items_query_1) == 1
    assert len(conv_items_query_2) == 2
    assert conv_items_query_1[0].content == "content-1"
    assert len(conv_items_query_fail) == 0


def test_list_conversation_items_until_id_found(pymongo_memory: AgentMemory):
    # Prepare
    delete_all_conversation_items(pymongo_memory, True)

    conv_id_1 = uuid()
    conv_id_2 = uuid()
    created_items: list[ConversationItem] = []

    FIND_ITEM_IDX = 7
    COUNT = 10
    LIMIT_COUNT = 3
    for i in range(0, COUNT):
        item = ConversationItem(
            conversation_id=conv_id_1,
            role="role",
            content=f"content-{i}",
            data={"key": "value"}
        )
        item_2 = ConversationItem(
            conversation_id=conv_id_2,
            role="role",
            content=f"content-{i}",
            data={"key": "value"}
        )
        created_items.append(item)
        pymongo_memory.conversation_items.create(item)
        pymongo_memory.conversation_items.create(item_2)

    find_item = created_items[FIND_ITEM_IDX]

    # Execute
    items = pymongo_memory.conversation_items.list_until_id_found(
        conversation_id=find_item.conversation_id,
        item_id=find_item.item_id
    )
    items_limit = pymongo_memory.conversation_items.list_until_id_found(
        conversation_id=find_item.conversation_id,
        item_id=find_item.item_id,
        limit=LIMIT_COUNT
    )

    # Check
    assert len(items) == FIND_ITEM_IDX + 1
    assert len(items_limit) == LIMIT_COUNT

    assert items[-1].item_id == created_items[FIND_ITEM_IDX].item_id
    assert items_limit[-1].item_id == created_items[FIND_ITEM_IDX].item_id

    assert items[0].item_id == created_items[0].item_id
    assert items_limit[0].item_id == created_items[FIND_ITEM_IDX - LIMIT_COUNT + 1].item_id


def test_update_conversation_item(pymongo_memory: AgentMemory):
    # Prepare
    item = ConversationItem(
        conversation_id=uuid(),
        role="role",
        content="content",
        data={"key": "value"}
    )
    item_created = pymongo_memory.conversation_items.create(item)

    # Execute
    item.role = "New role"
    item.content = "New content"
    item.data = {"keyNew": "valueNew"}

    pymongo_memory.conversation_items.update(item)
    item_updated = pymongo_memory.conversation_items.get(
        item_created.conversation_id,
        item_created.item_id
    )

    # Check
    assert item_updated is not None

    assert item_updated.role == item.role
    assert item_updated.content != item_created.content

    assert item_updated.data.get("key") is None
    assert item_updated.data.get("keyNew") is not None
    assert item_updated.data.get("keyNew") == item.data.get("keyNew")

    assert item_updated.created_at == item.created_at
    assert item_updated.updated_at > item_updated.created_at


def test_update_conversation_read_only_fields(pymongo_memory: AgentMemory):
    # Prepare
    item = ConversationItem(
        conversation_id=uuid(),
        role="role",
        content="content",
        data={"key": "value"}
    )
    item_created = pymongo_memory.conversation_items.create(item)

    # Execute
    item.created_at = None

    pymongo_memory.conversation_items.update(item)
    item_updated = pymongo_memory.conversation_items.get(item_created.conversation_id, item_created.item_id)

    # Check
    assert item_updated is not None

    assert item_updated.created_at != item.created_at
    assert item_updated.created_at == item_created.created_at


def test_delete_conversation(pymongo_memory: AgentMemory):
    # Prepare
    item = ConversationItem(
        conversation_id=uuid(),
        role="role",
        content="content",
        data={"key": "value"}
    )
    item_created = pymongo_memory.conversation_items.create(item)

    # Execute
    item_found = pymongo_memory.conversation_items.get(item_created.conversation_id, item_created.item_id)
    pymongo_memory.conversation_items.delete(item_created.conversation_id, item_created.item_id)

    # Check
    assert item_found is not None

    with pytest.raises(ObjectNotFoundError):
        pymongo_memory.conversation_items.get(item_created.conversation_id, item_created.item_id)
