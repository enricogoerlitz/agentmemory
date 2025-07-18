from agentmemory import AgentMemory
from agentmemory.schema.workflows import Workflow, WorkflowStatus
from agentmemory.connection.shortterm.cache import CacheRetrieveType
from agentmemory.connection.longterm.collections import Collection
from agentmemory.utils.dataclasses.default_factory_functions import uuid


def delete_all_workflows(memory: AgentMemory) -> None:
    for workflow in memory.workflows.list():
        memory.workflows.delete(workflow.workflow_id, cascade=True)


def clear_cache_complete(memory: AgentMemory) -> None:
    memory.cache.clear("*")


def prepare_test(memory: AgentMemory) -> None:
    delete_all_workflows(memory)
    clear_cache_complete(memory)


def test_cache_get_workflow(pymongo_cache_memory: AgentMemory):
    # Prepare
    prepare_test(pymongo_cache_memory)
    workflow = Workflow(
        conversation_item_id=uuid(),
        user_query="User query",
        status=WorkflowStatus.RUNNING,
        data={"key": "value"}
    )
    pymongo_cache_memory.workflows.create(workflow)

    # Execute
    workflow_get = pymongo_cache_memory.workflows.get(workflow.workflow_id)
    workflow_cache = pymongo_cache_memory.workflows.get(workflow.workflow_id)
    keys = pymongo_cache_memory.cache.keys("*")

    # Check
    assert len(keys) == 1
    assert f"id:{workflow.workflow_id}" in keys[0]
    assert f"type:{CacheRetrieveType.GET.value}" in keys[0]
    assert f"col:{Collection.WORKFLOWS.value}" in keys[0]

    assert workflow.user_query == workflow_get.user_query == workflow_cache.user_query
    assert workflow.status == workflow_get.status == workflow_cache.status
    assert (
        workflow.data.get("key") ==
        workflow_get.data.get("key") ==
        workflow_cache.data.get("key")
    )


def test_cache_list_workflow(pymongo_cache_memory: AgentMemory):
    # Prepare
    prepare_test(pymongo_cache_memory)

    COUNT = 10
    workflows: list[Workflow] = []
    for i in range(0, COUNT):
        workflow = Workflow(
            conversation_item_id=uuid(),
            user_query=f"User query-{i}",
            status=WorkflowStatus.RUNNING,
            data={"key": "value"}
        )
        workflows.append(workflow)
        pymongo_cache_memory.workflows.create(workflow)

    # Execute
    workflow_list = pymongo_cache_memory.workflows.list()
    workflow_list_cache = pymongo_cache_memory.workflows.list()
    keys = pymongo_cache_memory.cache.keys("*")

    # Check
    assert len(keys) == 1
    assert f"type:{CacheRetrieveType.LIST.value}" in keys[0]
    assert f"col:{Collection.WORKFLOWS.value}" in keys[0]

    for i, workflow in enumerate(workflows):
        assert workflow.user_query == workflow_list[i].user_query == workflow_list_cache[i].user_query
        assert workflow.status == workflow_list[i].status == workflow_list_cache[i].status
        assert (
            workflow.data.get("key") ==
            workflow_list[i].data.get("key") ==
            workflow_list_cache[i].data.get("key")
        )


def test_cache_list_by_conversation_item_id(pymongo_cache_memory: AgentMemory):
    return
    assert False


# TODO: list_by_conversation_item_id in _create, _update, _delete


def test_cache_workflow_clear_by_create(pymongo_cache_memory: AgentMemory):
    # Prepare
    prepare_test(pymongo_cache_memory)

    COUNT = 10
    workflows: list[Workflow] = []
    for i in range(0, COUNT):
        workflow = Workflow(
            conversation_item_id=uuid(),
            user_query=f"User query-{i}",
            status=WorkflowStatus.RUNNING,
            data={"key": "value"}
        )
        workflows.append(workflow)
        pymongo_cache_memory.workflows.create(workflow)

    # Execute & Check
    _ = pymongo_cache_memory.workflows.get(workflows[0].workflow_id)  # GET 1
    _ = pymongo_cache_memory.workflows.get(workflows[0].workflow_id)  # GET 1
    _ = pymongo_cache_memory.workflows.get(workflows[1].workflow_id)  # GET 2
    _ = pymongo_cache_memory.workflows.get(workflows[2].workflow_id)  # GET 3

    _ = pymongo_cache_memory.workflows.list()  # list 1
    _ = pymongo_cache_memory.workflows.list()  # list 1
    _ = pymongo_cache_memory.workflows.list(query={"title": "title-1"})  # list 2
    _ = pymongo_cache_memory.workflows.list(query={"title": "title-2"})  # list 3
    _ = pymongo_cache_memory.workflows.list(limit=2)  # list 4
    _ = pymongo_cache_memory.workflows.list(query={"title": "title-2"}, limit=2)  # list 5

    assert len(pymongo_cache_memory.cache.keys("*")) == (3 + 5)

    workflow_new = Workflow(conversation_item_id=uuid(), user_query="query", status=WorkflowStatus.ERROR)
    pymongo_cache_memory.workflows.create(workflow_new)
    keys = pymongo_cache_memory.cache.keys("*")

    assert len(keys) == (3 + 0)
    assert any(workflows[0].workflow_id in key for key in keys)
    assert any(workflows[1].workflow_id in key for key in keys)
    assert any(workflows[2].workflow_id in key for key in keys)


def test_cache_workflow_clear_by_update(pymongo_cache_memory: AgentMemory):
    # Prepare
    prepare_test(pymongo_cache_memory)

    COUNT = 10
    workflows: list[Workflow] = []
    for i in range(0, COUNT):
        workflow = Workflow(
            conversation_item_id=uuid(),
            user_query=f"User query-{i}",
            status=WorkflowStatus.RUNNING,
            data={"key": "value"}
        )
        workflows.append(workflow)
        pymongo_cache_memory.workflows.create(workflow)

    # Execute & Check
    GET_0_IDX = 0
    UPDATE_IDX = 5
    UPDATE_ID = workflows[UPDATE_IDX].workflow_id
    _ = pymongo_cache_memory.workflows.get(workflows[GET_0_IDX].workflow_id)  # GET 1
    _ = pymongo_cache_memory.workflows.get(workflows[GET_0_IDX].workflow_id)  # GET 1
    _ = pymongo_cache_memory.workflows.get(UPDATE_ID)  # GET 2

    _ = pymongo_cache_memory.workflows.list()  # list 1
    _ = pymongo_cache_memory.workflows.list()  # list 1
    _ = pymongo_cache_memory.workflows.list(query={"title": "title-1"})  # list 2
    _ = pymongo_cache_memory.workflows.list(query={"title": "title-2"})  # list 3
    _ = pymongo_cache_memory.workflows.list(limit=2)  # list 4
    _ = pymongo_cache_memory.workflows.list(query={"title": "title-2"}, limit=2)  # list 5

    assert len(pymongo_cache_memory.cache.keys("*")) == (2 + 5)

    workflow_updated = workflows[UPDATE_IDX]
    workflow_updated.user_query = "New query"

    pymongo_cache_memory.workflows.update(workflow_updated)
    keys = pymongo_cache_memory.cache.keys("*")

    assert len(keys) == (1 + 0)
    assert workflows[GET_0_IDX].workflow_id in keys[0]


def test_cache_workflow_clear_by_delete(pymongo_cache_memory: AgentMemory):
    # Prepare
    prepare_test(pymongo_cache_memory)

    COUNT = 10
    workflows: list[Workflow] = []
    for i in range(0, COUNT):
        workflow = Workflow(
            conversation_item_id=uuid(),
            user_query=f"User query-{i}",
            status=WorkflowStatus.RUNNING,
            data={"key": "value"}
        )
        workflows.append(workflow)
        pymongo_cache_memory.workflows.create(workflow)

    # Execute & Check
    GET_0_IDX = 0
    DELETE_ID = workflows[5].workflow_id
    _ = pymongo_cache_memory.workflows.get(workflows[GET_0_IDX].workflow_id)  # GET 1
    _ = pymongo_cache_memory.workflows.get(workflows[GET_0_IDX].workflow_id)  # GET 1
    _ = pymongo_cache_memory.workflows.get(DELETE_ID)  # GET 2

    _ = pymongo_cache_memory.workflows.list()  # list 1
    _ = pymongo_cache_memory.workflows.list()  # list 1
    _ = pymongo_cache_memory.workflows.list(query={"title": "title-1"})  # list 2
    _ = pymongo_cache_memory.workflows.list(query={"title": "title-2"})  # list 3
    _ = pymongo_cache_memory.workflows.list(limit=2)  # list 4
    _ = pymongo_cache_memory.workflows.list(query={"title": "title-2"}, limit=2)  # list 5

    assert len(pymongo_cache_memory.cache.keys("*")) == (2 + 5)

    pymongo_cache_memory.workflows.delete(DELETE_ID)
    keys = pymongo_cache_memory.cache.keys("*")

    assert len(keys) == (1 + 0)
    assert workflows[GET_0_IDX].workflow_id in keys[0]
