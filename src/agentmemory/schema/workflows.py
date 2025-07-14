from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from enum import Enum

from agentmemory.utils.dataclasses.default_factory_functions import (
    current_iso_datetime, uuid, empty_dict
)


class WorkflowStatus(str, Enum):
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"


@dataclass
class Workflow:
    conversation_item_id: str
    user_query: str
    status: WorkflowStatus
    _id: Optional[Any] = None
    workflow_id: str = field(default_factory=uuid)
    data: dict = field(default_factory=empty_dict)
    created_at: str = field(default_factory=current_iso_datetime)
    updated_at: str = field(default_factory=current_iso_datetime)

    def to_dict(self) -> dict:
        return asdict(self, dict_factory=dict)


@dataclass
class WorkflowStep:
    workflow_id: str
    name: str
    tool: str
    arguments: dict
    status: WorkflowStatus
    _id: Optional[Any] = None
    step_id: str = field(default_factory=uuid)
    result: Optional[str] = None
    logs: list[str] = field(default_factory=list)
    error: Optional[str] = None
    data: dict = field(default_factory=empty_dict)
    created_at: str = field(default_factory=current_iso_datetime)
    updated_at: str = field(default_factory=current_iso_datetime)

    def to_dict(self) -> dict:
        return asdict(self, dict_factory=dict)
