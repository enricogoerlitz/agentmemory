from typing import Iterator

from agentmemory.schema.workflows import Workflow, WorkflowStep
from agentmemory.connection.connection import AgentMemoryConnection
from agentmemory.utils.dataclasses.default_factory_functions import current_iso_datetime
from agentmemory.utils.validation.instance import check_isinstance


# TODO:
# - implement caching for get, list, create, update, delete methods
# - clear cache when workflow is created, updated or deleted

class Workflows:
    def __init__(self, con: AgentMemoryConnection):
        self._con = con

    def get(self, workflow_id: str, cache_cnf: dict = None) -> Workflow:
        return self._con.longterm.workflows().get(workflow_id)

    def list(self, query: dict = None, cache_cnf: dict = None) -> Iterator[Workflow]:
        return self._con.longterm.workflows().list(query)

    def list_by_conversation_id(self, conversation_item_id: str, query: dict = None, cache_cnf: dict = None) -> Iterator[Workflow]:
        return self._con.longterm.workflows().list_by_conversation_item_id(conversation_item_id, query)

    def create(self, workflow: Workflow) -> Workflow:
        check_isinstance(workflow, Workflow)
        return self._con.longterm.workflows().create(workflow)

    def update(self, workflow: Workflow) -> Workflow:
        check_isinstance(workflow, Workflow)
        workflow.updated_at = current_iso_datetime()
        update_data = {
            "status": workflow.status,
            "user_query": workflow.user_query,
            "data": workflow.data,
            "updated_at": workflow.updated_at
        }
        self._con.longterm.workflows().update(workflow.workflow_id, update_data)
        return workflow

    def delete(self, workflow_id: str, cascade: bool = False) -> None:
        return self._con.longterm.workflows().delete(workflow_id, cascade)


class WorkflowSteps:
    def __init__(self, con: AgentMemoryConnection):
        self._con = con

    def get(self, workflow_id: str, step_id: str, cache_cnf: dict = None) -> WorkflowStep:
        return self._con.longterm.workflow_steps().get(workflow_id, step_id)

    def list(self, query: dict = None, cache_cnf: dict = None) -> Iterator[WorkflowStep]:
        return self._con.longterm.workflow_steps().list(query)

    def list_by_workflow_id(self, workflow_id: str, query: dict = None, cache_cnf: dict = None) -> Iterator[WorkflowStep]:
        return self._con.longterm.workflow_steps().list_by_workflow_id(workflow_id, query)

    def create(self, step: WorkflowStep) -> WorkflowStep:
        check_isinstance(step, WorkflowStep)
        return self._con.longterm.workflow_steps().create(step)

    def update(self, step: WorkflowStep) -> WorkflowStep:
        check_isinstance(step, WorkflowStep)
        step.updated_at = current_iso_datetime()
        update_data = {
            "name": step.name,
            "tool": step.tool,
            "arguments": step.arguments,
            "status": step.status,
            "result": step.result,
            "logs": step.logs,
            "error": step.error,
            "data": step.data,
            "updated_at": step.updated_at
        }
        self._con.longterm.workflow_steps().update(
            workflow_id=step.workflow_id,
            step_id=step.step_id,
            update_data=update_data
        )
        return step

    def delete(self, workflow_id: str, step_id: str) -> None:
        return self._con.longterm.workflow_steps().delete(workflow_id, step_id)
