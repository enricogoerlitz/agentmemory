import pytest

from agentmemory import AgentMemory
from agentmemory.schema.workflows import Workflow, WorkflowStep, WorkflowStatus
from agentmemory.exc.errors import ObjectNotFoundError
from agentmemory.utils.dataclasses.default_factory_functions import uuid


def delete_all_workflows(memory: AgentMemory, cascade: bool) -> None:
    for workflow in memory.workflows.list():
        memory.workflows.delete(workflow.workflow_id, cascade=cascade)


def test_create_workflow(pymongo_memory: AgentMemory):
    # Prepare
    workflow = Workflow(
        conversation_item_id=uuid(),
        user_query="User query",
        status=WorkflowStatus.RUNNING,
        data={"key": "value"}
    )

    # Execute
    workflow_created = pymongo_memory.workflows.create(workflow)

    # Check
    assert workflow_created is not None

    assert workflow_created._id is not None
    assert workflow_created.workflow_id is not None
    assert workflow_created.conversation_item_id is not None
    assert workflow_created.created_at is not None
    assert workflow_created.updated_at is not None

    assert workflow_created._id == workflow._id
    assert workflow_created.workflow_id == workflow.workflow_id
    assert workflow_created.conversation_item_id == workflow.conversation_item_id
    assert workflow_created.user_query == workflow.user_query
    assert workflow_created.status == workflow.status
    assert workflow_created.data.get("key") == workflow.data.get("key")
    assert workflow_created.created_at == workflow.created_at
    assert workflow_created.updated_at == workflow.updated_at


def test_get_workflow(pymongo_memory: AgentMemory):
    # Prepare
    workflow = Workflow(
        conversation_item_id=uuid(),
        user_query="User query",
        status=WorkflowStatus.RUNNING
    )
    _ = pymongo_memory.workflows.create(workflow)

    # Execute
    workflow_get = pymongo_memory.workflows.get(workflow.workflow_id)

    # Check
    assert workflow_get is not None

    assert workflow_get._id == workflow._id
    assert workflow_get.workflow_id == workflow.workflow_id
    assert workflow_get.conversation_item_id == workflow.conversation_item_id
    assert workflow_get.user_query == workflow.user_query
    assert workflow_get.status == workflow.status
    assert workflow_get.created_at == workflow.created_at
    assert workflow_get.updated_at == workflow.updated_at


def test_get_workflow_not_found(pymongo_memory: AgentMemory):
    # Prepare
    not_existing_workflow_id = uuid()

    # Execute & Check
    with pytest.raises(ObjectNotFoundError):
        pymongo_memory.workflows.get(not_existing_workflow_id)


def test_list_workflows(pymongo_memory: AgentMemory):
    # Prepare
    delete_all_workflows(pymongo_memory, True)

    COUNT = 5
    LIMIT_COUNT = 3
    for i in range(0, COUNT):
        pymongo_memory.workflows.create(
            workflow=Workflow(
                conversation_item_id=uuid(),
                user_query=f"User query XYZ-{i}",
                status=WorkflowStatus.RUNNING
            )
        )

    # Execute
    workflows = pymongo_memory.workflows.list()
    workflows_limit = pymongo_memory.workflows.list(limit=LIMIT_COUNT)
    workflows_query = pymongo_memory.workflows.list(query={"user_query": "User query XYZ-1"})
    workflows_query_fail = pymongo_memory.workflows.list(query={"user_query": "XXX"})

    # Check
    assert len(workflows) == COUNT
    assert len(workflows_limit) == LIMIT_COUNT
    assert len(workflows_query) == 1
    assert workflows_query[0].user_query == "User query XYZ-1"
    assert len(workflows_query_fail) == 0


def test_list_workflows_by_conversation_item_id(pymongo_memory: AgentMemory):
    # Prepare
    delete_all_workflows(pymongo_memory, True)

    conv_item_id_1 = uuid()
    conv_item_id_2 = uuid()
    COUNT = 5
    LIMIT_COUNT = 3
    for item_id in [conv_item_id_1, conv_item_id_2]:
        for i in range(0, COUNT):
            pymongo_memory.workflows.create(
                workflow=Workflow(
                    conversation_item_id=item_id,
                    user_query=f"User query XYZ-{i}",
                    status=WorkflowStatus.RUNNING
                )
            )

    pymongo_memory.workflows.create(
        workflow=Workflow(
            conversation_item_id=conv_item_id_2,
            user_query="User query XYZ-1",
            status=WorkflowStatus.RUNNING
        )
    )

    # Execute
    workflows_item_1 = pymongo_memory.workflows.list_by_conversation_item_id(conv_item_id_1)
    workflows_item_2 = pymongo_memory.workflows.list_by_conversation_item_id(conv_item_id_2)
    workflows_limit = pymongo_memory.workflows.list_by_conversation_item_id(conv_item_id_1, limit=LIMIT_COUNT)
    workflows_query_1 = pymongo_memory.workflows.list_by_conversation_item_id(conv_item_id_1, query={"user_query": "User query XYZ-1"})
    workflows_query_2 = pymongo_memory.workflows.list_by_conversation_item_id(conv_item_id_2, query={"user_query": "User query XYZ-1"})
    workflows_query_fail = pymongo_memory.workflows.list_by_conversation_item_id(conv_item_id_1, query={"user_query": "XXX"})

    # Check
    assert len(workflows_item_1) == COUNT
    assert len(workflows_item_2) == COUNT + 1

    assert len(workflows_limit) == LIMIT_COUNT

    assert len(workflows_query_1) == 1
    assert len(workflows_query_2) == 2
    assert workflows_query_1[0].user_query == "User query XYZ-1"
    assert len(workflows_query_fail) == 0


def test_update_workflow(pymongo_memory: AgentMemory):
    # Prepare
    workflow = Workflow(
        conversation_item_id=uuid(),
        user_query="User query",
        status=WorkflowStatus.RUNNING,
        data={"key": "value"}
    )
    workflow_created = pymongo_memory.workflows.create(workflow)

    # Execute
    workflow.user_query = "New query"
    workflow.status = WorkflowStatus.SUCCESS
    workflow.data = {"keyNew": "valueNew"}

    pymongo_memory.workflows.update(workflow)
    workflow_updated = pymongo_memory.workflows.get(workflow_created.workflow_id)

    # Check
    assert workflow_updated is not None
    assert workflow_updated.data.get("key") is None
    assert workflow_updated.data.get("keyNew") is not None

    assert workflow_updated.user_query == workflow.user_query
    assert workflow_updated.status == workflow.status
    assert workflow_updated.data.get("keyNew") == workflow.data.get("keyNew")

    assert workflow_updated.created_at == workflow.created_at
    assert workflow_updated.updated_at > workflow_updated.created_at


def test_update_workflow_read_only_fields(pymongo_memory: AgentMemory):
    # Prepare
    workflow = Workflow(
        conversation_item_id=uuid(),
        user_query="User query",
        status=WorkflowStatus.RUNNING
    )
    workflow_created = pymongo_memory.workflows.create(workflow)

    # Execute
    workflow.conversation_item_id = None
    workflow.created_at = None

    pymongo_memory.workflows.update(workflow)
    workflow_updated = pymongo_memory.workflows.get(workflow_created.workflow_id)

    # Check
    assert workflow_updated is not None

    assert workflow_updated.created_at != workflow.created_at
    assert workflow_updated.conversation_item_id != workflow.conversation_item_id

    assert workflow_updated.conversation_item_id == workflow_created.conversation_item_id
    assert workflow_updated.created_at == workflow_created.created_at


def test_delete_workflow(pymongo_memory: AgentMemory):
    # Prepare
    workflow = Workflow(
        conversation_item_id=uuid(),
        user_query="User query",
        status=WorkflowStatus.RUNNING
    )
    workflow_created = pymongo_memory.workflows.create(workflow)

    # Execute
    workflow_found = pymongo_memory.workflows.get(workflow_created.workflow_id)
    pymongo_memory.workflows.delete(workflow_created.workflow_id)

    # Check
    assert workflow_found is not None

    with pytest.raises(ObjectNotFoundError):
        pymongo_memory.workflows.get(workflow_created.workflow_id)


def test_delete_workflow_cascade(pymongo_memory: AgentMemory):
    # Prepare
    workflow_1 = Workflow(
        conversation_item_id=uuid(),
        user_query="User query",
        status=WorkflowStatus.RUNNING
    )
    workflow_2 = Workflow(
        conversation_item_id=uuid(),
        user_query="User query 2",
        status=WorkflowStatus.RUNNING
    )
    workflow_created_1 = pymongo_memory.workflows.create(workflow_1)
    workflow_created_2 = pymongo_memory.workflows.create(workflow_2)

    ITEM_COUNT = 3

    for i in range(0, ITEM_COUNT):
        pymongo_memory.workflow_steps.create(
            step=WorkflowStep(
                workflow_id=workflow_created_1.workflow_id,
                name=f"Name-{i}-1",
                tool=f"Tool-{i}-1",
                arguments={
                    "arg1": "value1"
                },
                status=WorkflowStatus.SUCCESS
            )
        )
        pymongo_memory.workflow_steps.create(
            step=WorkflowStep(
                workflow_id=workflow_created_2.workflow_id,
                name=f"Name-{i}-2",
                tool=f"Tool-{i}-2",
                arguments={
                    "arg1": "value1"
                },
                status=WorkflowStatus.SUCCESS
            )
        )

    # Execute
    pymongo_memory.workflows.delete(workflow_created_1.workflow_id, cascade=True)
    pymongo_memory.workflows.delete(workflow_created_2.workflow_id, cascade=False)
    items_1 = pymongo_memory.workflow_steps.list_by_workflow_id(workflow_created_1.workflow_id)
    items_2 = pymongo_memory.workflow_steps.list_by_workflow_id(workflow_created_2.workflow_id)

    # Check
    assert len(items_1) == 0
    assert len(items_2) == ITEM_COUNT
