from agentmemory import AgentMemory
from agentmemory.schema.conversations import Conversation
from agentmemory.connection.shortterm.cache import CacheRetrieveType
from agentmemory.connection.longterm.collections import Collection


def delete_all_conversations(memory: AgentMemory) -> None:
    for conversation in memory.conversations.list():
        memory.conversations.delete(conversation.conversation_id, cascade=True)


def clear_cache_complete(memory: AgentMemory) -> None:
    memory.cache.clear("*")


def prepare_test(memory: AgentMemory) -> None:
    delete_all_conversations(memory)
    clear_cache_complete(memory)


def test_is_cache_enabled(pymongo_cache_memory: AgentMemory):
    assert pymongo_cache_memory.con.shortterm is not None


def test_cache_get_conversation(pymongo_cache_memory: AgentMemory):
    # Prepare
    prepare_test(pymongo_cache_memory)
    conv = Conversation(
        title="title",
        data={"key": "value"}
    )
    pymongo_cache_memory.conversations.create(conv)

    # Execute
    conv_get = pymongo_cache_memory.conversations.get(conv.conversation_id)
    conv_cache = pymongo_cache_memory.conversations.get(conv.conversation_id)
    keys = pymongo_cache_memory.cache.keys("*")

    # Check
    assert len(keys) == 1
    assert f"id:{conv.conversation_id}" in keys[0]
    assert f"type:{CacheRetrieveType.GET.value}" in keys[0]
    assert f"col:{Collection.CONVERSATIONS.value}" in keys[0]

    assert conv.title == conv_get.title == conv_cache.title
    assert (
        conv.data.get("key") ==
        conv_get.data.get("key") ==
        conv_cache.data.get("key")
    )


def test_cache_list_conversation(pymongo_cache_memory: AgentMemory):
    # Prepare
    prepare_test(pymongo_cache_memory)

    COUNT = 10
    conversations: list[Conversation] = []
    for i in range(0, COUNT):
        conv = Conversation(
            title=f"title-{i}",
            data={"key": f"value-{i}"}
        )
        conversations.append(conv)
        pymongo_cache_memory.conversations.create(conv)

    # Execute
    conv_list = pymongo_cache_memory.conversations.list()
    conv_list_cache = pymongo_cache_memory.conversations.list()
    keys = pymongo_cache_memory.cache.keys("*")

    # Check
    assert len(keys) == 1
    assert f"type:{CacheRetrieveType.LIST.value}" in keys[0]
    assert f"col:{Collection.CONVERSATIONS.value}" in keys[0]

    for i, conv in enumerate(conversations):
        assert conv.title == conv_list[i].title == conv_list_cache[i].title
        assert (
            conv.data.get("key") ==
            conv_list[i].data.get("key") ==
            conv_list_cache[i].data.get("key")
        )


def test_cache_conversation_clear_by_create(pymongo_cache_memory: AgentMemory):
    # Prepare
    prepare_test(pymongo_cache_memory)

    COUNT = 10
    conversations: list[Conversation] = []
    for i in range(0, COUNT):
        conv = Conversation(
            title=f"title-{i}",
            data={"key": f"value-{i}"}
        )
        conversations.append(conv)
        pymongo_cache_memory.conversations.create(conv)

    # Execute & Check
    _ = pymongo_cache_memory.conversations.get(conversations[0].conversation_id)  # GET 1
    _ = pymongo_cache_memory.conversations.get(conversations[0].conversation_id)  # GET 1
    _ = pymongo_cache_memory.conversations.get(conversations[1].conversation_id)  # GET 2
    _ = pymongo_cache_memory.conversations.get(conversations[2].conversation_id)  # GET 3

    _ = pymongo_cache_memory.conversations.list()  # list 1
    _ = pymongo_cache_memory.conversations.list()  # list 1
    _ = pymongo_cache_memory.conversations.list(query={"title": "title-1"})  # list 2
    _ = pymongo_cache_memory.conversations.list(query={"title": "title-2"})  # list 3
    _ = pymongo_cache_memory.conversations.list(limit=2)  # list 4
    _ = pymongo_cache_memory.conversations.list(query={"title": "title-2"}, limit=2)  # list 5

    assert len(pymongo_cache_memory.cache.keys("*")) == (3 + 5)

    conv_new = Conversation(title="New title")
    pymongo_cache_memory.conversations.create(conv_new)
    keys = pymongo_cache_memory.cache.keys("*")

    assert len(keys) == (3 + 0)
    assert any(conversations[0].conversation_id in key for key in keys)
    assert any(conversations[1].conversation_id in key for key in keys)
    assert any(conversations[2].conversation_id in key for key in keys)


def test_cache_conversation_clear_by_update(pymongo_cache_memory: AgentMemory):
    # Prepare
    prepare_test(pymongo_cache_memory)

    COUNT = 10
    conversations: list[Conversation] = []
    for i in range(0, COUNT):
        conv = Conversation(
            title=f"title-{i}",
            data={"key": f"value-{i}"}
        )
        conversations.append(conv)
        pymongo_cache_memory.conversations.create(conv)

    # Execute & Check
    GET_0_IDX = 0
    UPDATE_IDX = 5
    UPDATE_ID = conversations[UPDATE_IDX].conversation_id
    _ = pymongo_cache_memory.conversations.get(conversations[GET_0_IDX].conversation_id)  # GET 1
    _ = pymongo_cache_memory.conversations.get(conversations[GET_0_IDX].conversation_id)  # GET 1
    _ = pymongo_cache_memory.conversations.get(UPDATE_ID)  # GET 2

    _ = pymongo_cache_memory.conversations.list()  # list 1
    _ = pymongo_cache_memory.conversations.list()  # list 1
    _ = pymongo_cache_memory.conversations.list(query={"title": "title-1"})  # list 2
    _ = pymongo_cache_memory.conversations.list(query={"title": "title-2"})  # list 3
    _ = pymongo_cache_memory.conversations.list(limit=2)  # list 4
    _ = pymongo_cache_memory.conversations.list(query={"title": "title-2"}, limit=2)  # list 5

    assert len(pymongo_cache_memory.cache.keys("*")) == (2 + 5)

    conv_updated = conversations[UPDATE_IDX]
    conv_updated.title = "New title"

    pymongo_cache_memory.conversations.update(conv_updated)
    keys = pymongo_cache_memory.cache.keys("*")

    assert len(keys) == (1 + 0)
    assert conversations[GET_0_IDX].conversation_id in keys[0]


def test_cache_conversation_clear_by_delete(pymongo_cache_memory: AgentMemory):
    # Prepare
    prepare_test(pymongo_cache_memory)

    COUNT = 10
    conversations: list[Conversation] = []
    for i in range(0, COUNT):
        conv = Conversation(
            title=f"title-{i}",
            data={"key": f"value-{i}"}
        )
        conversations.append(conv)
        pymongo_cache_memory.conversations.create(conv)

    # Execute & Check
    GET_0_IDX = 0
    DELETE_ID = conversations[5].conversation_id
    _ = pymongo_cache_memory.conversations.get(conversations[GET_0_IDX].conversation_id)  # GET 1
    _ = pymongo_cache_memory.conversations.get(conversations[GET_0_IDX].conversation_id)  # GET 1
    _ = pymongo_cache_memory.conversations.get(DELETE_ID)  # GET 2

    _ = pymongo_cache_memory.conversations.list()  # list 1
    _ = pymongo_cache_memory.conversations.list()  # list 1
    _ = pymongo_cache_memory.conversations.list(query={"title": "title-1"})  # list 2
    _ = pymongo_cache_memory.conversations.list(query={"title": "title-2"})  # list 3
    _ = pymongo_cache_memory.conversations.list(limit=2)  # list 4
    _ = pymongo_cache_memory.conversations.list(query={"title": "title-2"}, limit=2)  # list 5

    assert len(pymongo_cache_memory.cache.keys("*")) == (2 + 5)

    pymongo_cache_memory.conversations.delete(DELETE_ID)
    keys = pymongo_cache_memory.cache.keys("*")

    assert len(keys) == (1 + 0)
    assert conversations[GET_0_IDX].conversation_id in keys[0]
