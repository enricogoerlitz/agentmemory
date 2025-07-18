from agentmemory import AgentMemory
from agentmemory.schema.workflows import WorkflowStep, WorkflowStatus
from agentmemory.connection.shortterm.cache import CacheRetrieveType
from agentmemory.connection.longterm.collections import Collection
from agentmemory.utils.dataclasses.default_factory_functions import uuid


def delete_all_workflow_steps(memory: AgentMemory) -> None:
    for step in memory.workflow_steps.list():
        memory.workflow_steps.delete(step.workflow_id, step.step_id)


def clear_cache_complete(memory: AgentMemory) -> None:
    memory.cache.clear("*")


def prepare_test(memory: AgentMemory) -> None:
    delete_all_workflow_steps(memory)
    clear_cache_complete(memory)


def test_cache_get_workflow_step(pymongo_cache_memory: AgentMemory):
    # Prepare
    prepare_test(pymongo_cache_memory)
    step = WorkflowStep(
        workflow_id=uuid(),
        name="name",
        tool="tool",
        arguments={"arg1": "value1"},
        status=WorkflowStatus.SUCCESS
    )
    pymongo_cache_memory.workflow_steps.create(step)

    # Execute
    workflow_step_get = pymongo_cache_memory.workflow_steps.get(step.workflow_id, step.step_id)
    workflow_step_cache = pymongo_cache_memory.workflow_steps.get(step.workflow_id, step.step_id)
    keys = pymongo_cache_memory.cache.keys("*")

    # Check
    assert len(keys) == 1
    assert f"id:{step.workflow_id},{step.step_id}" in keys[0]
    assert f"type:{CacheRetrieveType.GET.value}" in keys[0]
    assert f"col:{Collection.WORKFLOW_STEPS.value}" in keys[0]

    assert step.name == workflow_step_get.name == workflow_step_cache.name
    assert step.tool == workflow_step_get.tool == workflow_step_cache.tool
    assert step.status == workflow_step_get.status == workflow_step_cache.status
    assert (
        step.arguments.get("key") ==
        workflow_step_get.arguments.get("key") ==
        workflow_step_cache.arguments.get("key")
    )


def test_cache_list_workflow_step(pymongo_cache_memory: AgentMemory):
    # Prepare
    prepare_test(pymongo_cache_memory)

    COUNT = 10
    workflow_steps: list[WorkflowStep] = []
    for i in range(0, COUNT):
        step = WorkflowStep(
            workflow_id=uuid(),
            name=f"name-{i}",
            tool="tool",
            arguments={"arg1": "value1"},
            status=WorkflowStatus.SUCCESS
        )
        workflow_steps.append(step)
        pymongo_cache_memory.workflow_steps.create(step)

    # Execute
    workflow_step_list = pymongo_cache_memory.workflow_steps.list()
    workflow_step_list_cache = pymongo_cache_memory.workflow_steps.list()
    keys = pymongo_cache_memory.cache.keys("*")

    # Check
    assert len(keys) == 1
    assert f"type:{CacheRetrieveType.LIST.value}" in keys[0]
    assert f"col:{Collection.WORKFLOW_STEPS.value}" in keys[0]

    for i, step in enumerate(workflow_steps):
        assert step.name == workflow_step_list[i].name == workflow_step_list_cache[i].name
        assert step.tool == workflow_step_list[i].tool == workflow_step_list_cache[i].tool
        assert step.status == workflow_step_list[i].status == workflow_step_list_cache[i].status
        assert (
            step.arguments.get("key") ==
            workflow_step_list[i].arguments.get("key") ==
            workflow_step_list_cache[i].arguments.get("key")
        )


def test_cache_list_workflow_steps_by_conversation_item_id(pymongo_cache_memory: AgentMemory):
    # Prepare
    prepare_test(pymongo_cache_memory)

    workflow_id_1 = uuid()
    workflow_id_2 = uuid()

    COUNT = 10
    workflow_steps_1: list[WorkflowStep] = []
    workflow_steps_2: list[WorkflowStep] = []
    for i in range(0, COUNT):
        workflow_step_1 = WorkflowStep(
            workflow_id=workflow_id_1,
            name=f"name-{i}-1",
            tool="tool",
            arguments={"arg1": "value1"},
            status=WorkflowStatus.SUCCESS
        )
        workflow_step_2 = WorkflowStep(
            workflow_id=workflow_id_2,
            name=f"name-{i}-2",
            tool="tool",
            arguments={"arg1": "value1"},
            status=WorkflowStatus.SUCCESS
        )
        workflow_steps_1.append(workflow_step_1)
        workflow_steps_2.append(workflow_step_2)
        pymongo_cache_memory.workflow_steps.create(workflow_step_1)
        pymongo_cache_memory.workflow_steps.create(workflow_step_2)

    # Execute
    workflow_step_list_1 = pymongo_cache_memory.workflow_steps.list_by_workflow_id(workflow_id_1)
    workflow_step_list_cache_1 = pymongo_cache_memory.workflow_steps.list_by_workflow_id(workflow_id_1)
    workflow_step_list_2 = pymongo_cache_memory.workflow_steps.list_by_workflow_id(workflow_id_2)
    workflow_step_list_cache_2 = pymongo_cache_memory.workflow_steps.list_by_workflow_id(workflow_id_2)
    keys = pymongo_cache_memory.cache.keys("*")

    # Check
    assert len(keys) == 2
    assert any(workflow_id_1 in key for key in keys)
    assert any(workflow_id_2 in key for key in keys)

    assert all(f"type:{CacheRetrieveType.LIST_BY_ANCHOR.value}" in key for key in keys)
    assert all(f"col:{Collection.WORKFLOW_STEPS.value}" in key for key in keys)

    assert len(pymongo_cache_memory.workflow_steps.list()) == COUNT * 2
    assert len(workflow_step_list_1) == COUNT
    assert len(workflow_step_list_2) == COUNT
    assert len(workflow_step_list_cache_1) == COUNT
    assert len(workflow_step_list_cache_2) == COUNT

    for i, step in enumerate(workflow_steps_1):
        assert step.name == workflow_step_list_1[i].name == workflow_step_list_cache_1[i].name
        assert step.tool == workflow_step_list_1[i].tool == workflow_step_list_cache_1[i].tool
        assert step.status == workflow_step_list_1[i].status == workflow_step_list_cache_1[i].status
        assert (
            step.arguments.get("key") ==
            workflow_step_list_1[i].arguments.get("key") ==
            workflow_step_list_cache_1[i].arguments.get("key")
        )

    for i, step in enumerate(workflow_steps_2):
        assert step.name == workflow_step_list_2[i].name == workflow_step_list_cache_2[i].name
        assert step.tool == workflow_step_list_2[i].tool == workflow_step_list_cache_2[i].tool
        assert step.status == workflow_step_list_2[i].status == workflow_step_list_cache_2[i].status
        assert (
            step.arguments.get("key") ==
            workflow_step_list_2[i].arguments.get("key") ==
            workflow_step_list_cache_2[i].arguments.get("key")
        )


def test_cache_workflow_step_clear_by_create(pymongo_cache_memory: AgentMemory):
    # Prepare
    prepare_test(pymongo_cache_memory)

    random_id = uuid()

    COUNT = 10
    workflow_steps: list[WorkflowStep] = []
    for i in range(0, COUNT):
        step = WorkflowStep(
            workflow_id=uuid(),
            name=f"name-{i}-1",
            tool="tool",
            arguments={"arg1": "value1"},
            status=WorkflowStatus.SUCCESS
        )
        workflow_steps.append(step)
        pymongo_cache_memory.workflow_steps.create(step)

    # Execute & Check
    _ = pymongo_cache_memory.workflow_steps.get(
        workflow_id=workflow_steps[0].workflow_id,
        step_id=workflow_steps[0].step_id
    )  # GET 1
    _ = pymongo_cache_memory.workflow_steps.get(
        workflow_id=workflow_steps[0].workflow_id,
        step_id=workflow_steps[0].step_id
    )  # GET 1
    _ = pymongo_cache_memory.workflow_steps.get(
        workflow_id=workflow_steps[1].workflow_id,
        step_id=workflow_steps[1].step_id
    )  # GET 2
    _ = pymongo_cache_memory.workflow_steps.get(
        workflow_id=workflow_steps[2].workflow_id,
        step_id=workflow_steps[2].step_id
    )  # GET 3

    _ = pymongo_cache_memory.workflow_steps.list()  # list 1
    _ = pymongo_cache_memory.workflow_steps.list()  # list 1
    _ = pymongo_cache_memory.workflow_steps.list(query={"title": "title-1"})  # list 2
    _ = pymongo_cache_memory.workflow_steps.list(query={"title": "title-2"})  # list 3
    _ = pymongo_cache_memory.workflow_steps.list(limit=2)  # list 4
    _ = pymongo_cache_memory.workflow_steps.list(query={"title": "title-2"}, limit=2)  # list 5

    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(random_id)  # list_anchor 1
    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(random_id)  # list_anchor 1
    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(random_id, query={"title": "title-1"})  # list_anchor 2
    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(random_id, query={"title": "title-2"})  # list_anchor 3
    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(random_id, limit=2)  # list_anchor 4
    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(random_id, query={"title": "title-2"}, limit=2)  # list_anchor 5

    assert len(pymongo_cache_memory.cache.keys("*")) == (3 + 5 + 5)

    workflow_step_new = WorkflowStep(workflow_id=uuid(), name="name", tool="tool", status=WorkflowStatus.ERROR, arguments={})
    pymongo_cache_memory.workflow_steps.create(workflow_step_new)
    keys = pymongo_cache_memory.cache.keys("*")

    assert len(keys) == (3 + 5)
    assert any(workflow_steps[0].workflow_id in key for key in keys)
    assert any(workflow_steps[1].workflow_id in key for key in keys)
    assert any(workflow_steps[2].workflow_id in key for key in keys)
    assert len([key for key in keys if random_id in key]) == 5


def test_cache_workflow_step_clear_by_update(pymongo_cache_memory: AgentMemory):
    # Prepare
    prepare_test(pymongo_cache_memory)

    random_id = uuid()

    COUNT = 10
    workflow_steps: list[WorkflowStep] = []
    for i in range(0, COUNT):
        step = WorkflowStep(
            workflow_id=uuid(),
            name=f"name-{i}-1",
            tool="tool",
            arguments={"arg1": "value1"},
            status=WorkflowStatus.SUCCESS
        )
        workflow_steps.append(step)
        pymongo_cache_memory.workflow_steps.create(step)

    # Execute & Check
    GET_0_IDX = 0
    UPDATE_IDX = 5
    UPDATE_STEP = workflow_steps[UPDATE_IDX]
    _ = pymongo_cache_memory.workflow_steps.get(
        workflow_id=workflow_steps[GET_0_IDX].workflow_id,
        step_id=workflow_steps[GET_0_IDX].step_id
    )  # GET 1
    _ = pymongo_cache_memory.workflow_steps.get(
        workflow_id=workflow_steps[GET_0_IDX].workflow_id,
        step_id=workflow_steps[GET_0_IDX].step_id
    )  # GET 1
    _ = pymongo_cache_memory.workflow_steps.get(UPDATE_STEP.workflow_id, UPDATE_STEP.step_id)  # GET 2

    _ = pymongo_cache_memory.workflow_steps.list()  # list 1
    _ = pymongo_cache_memory.workflow_steps.list()  # list 1
    _ = pymongo_cache_memory.workflow_steps.list(query={"title": "title-1"})  # list 2
    _ = pymongo_cache_memory.workflow_steps.list(query={"title": "title-2"})  # list 3
    _ = pymongo_cache_memory.workflow_steps.list(limit=2)  # list 4
    _ = pymongo_cache_memory.workflow_steps.list(query={"title": "title-2"}, limit=2)  # list 5

    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(UPDATE_STEP.workflow_id)  # list_anchor 1 / 0
    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(random_id)  # list_anchor 2 / 1
    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(random_id, query={"title": "title-1"})  # list_anchor 3 / 2
    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(random_id, query={"title": "title-2"})  # list_anchor 4 / 3
    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(random_id, limit=2)  # list_anchor 5 / 4
    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(random_id, query={"title": "title-2"}, limit=2)  # list_anchor 6 / 5

    assert len(pymongo_cache_memory.cache.keys("*")) == (2 + 5 + 6)

    UPDATE_STEP.name = "New name"

    pymongo_cache_memory.workflow_steps.update(UPDATE_STEP)
    keys = pymongo_cache_memory.cache.keys("*")

    assert len(keys) == (1 + 5)
    assert any(workflow_steps[GET_0_IDX].workflow_id in key for key in keys)
    assert not any(UPDATE_STEP.workflow_id in key for key in keys)
    assert len([key for key in keys if random_id in key]) == 5


def test_cache_workflow_step_clear_by_delete(pymongo_cache_memory: AgentMemory):
    # Prepare
    prepare_test(pymongo_cache_memory)

    random_id = uuid()

    COUNT = 10
    workflow_steps: list[WorkflowStep] = []
    for i in range(0, COUNT):
        step = WorkflowStep(
            workflow_id=uuid(),
            name=f"name-{i}-1",
            tool="tool",
            arguments={"arg1": "value1"},
            status=WorkflowStatus.SUCCESS
        )
        workflow_steps.append(step)
        pymongo_cache_memory.workflow_steps.create(step)

    # Execute & Check
    GET_0_IDX = 0
    UPDATE_IDX = 5
    UPDATE_STEP = workflow_steps[UPDATE_IDX]
    _ = pymongo_cache_memory.workflow_steps.get(
        workflow_id=workflow_steps[GET_0_IDX].workflow_id,
        step_id=workflow_steps[GET_0_IDX].step_id
    )  # GET 1
    _ = pymongo_cache_memory.workflow_steps.get(
        workflow_id=workflow_steps[GET_0_IDX].workflow_id,
        step_id=workflow_steps[GET_0_IDX].step_id
    )  # GET 1
    _ = pymongo_cache_memory.workflow_steps.get(UPDATE_STEP.workflow_id, UPDATE_STEP.step_id)  # GET 2

    _ = pymongo_cache_memory.workflow_steps.list()  # list 1
    _ = pymongo_cache_memory.workflow_steps.list()  # list 1
    _ = pymongo_cache_memory.workflow_steps.list(query={"title": "title-1"})  # list 2
    _ = pymongo_cache_memory.workflow_steps.list(query={"title": "title-2"})  # list 3
    _ = pymongo_cache_memory.workflow_steps.list(limit=2)  # list 4
    _ = pymongo_cache_memory.workflow_steps.list(query={"title": "title-2"}, limit=2)  # list 5

    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(UPDATE_STEP.workflow_id)  # list_anchor 1 / 0
    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(random_id)  # list_anchor 2 / 1
    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(random_id, query={"title": "title-1"})  # list_anchor 3 / 2
    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(random_id, query={"title": "title-2"})  # list_anchor 4 / 3
    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(random_id, limit=2)  # list_anchor 5 / 4
    _ = pymongo_cache_memory.workflow_steps.list_by_workflow_id(random_id, query={"title": "title-2"}, limit=2)  # list_anchor 6 / 5

    assert len(pymongo_cache_memory.cache.keys("*")) == (2 + 5 + 6)

    pymongo_cache_memory.workflow_steps.delete(UPDATE_STEP.workflow_id, UPDATE_STEP.step_id)
    keys = pymongo_cache_memory.cache.keys("*")

    assert len(keys) == (1 + 5)
    assert any(workflow_steps[GET_0_IDX].workflow_id in key for key in keys)
    assert not any(UPDATE_STEP.workflow_id in key for key in keys)
    assert len([key for key in keys if random_id in key]) == 5
