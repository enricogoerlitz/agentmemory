from dataclasses import dataclass, field, asdict
from typing import Any, Optional

from agentmemory.utils.dataclasses.default_factory_functions import (
    current_iso_datetime, uuid, empty_dict
)


@dataclass
class Conversation:
    title: str
    _id: Optional[Any] = None
    conversation_id: str = field(default_factory=uuid)
    data: dict = field(default_factory=empty_dict)
    created_at: str = field(default_factory=current_iso_datetime)
    updated_at: str = field(default_factory=current_iso_datetime)

    def to_dict(self) -> dict:
        return asdict(self, dict_factory=dict)


@dataclass
class ConversationItem:
    conversation_id: str
    role: str
    content: str
    _id: Optional[Any] = None
    item_id: str = field(default_factory=uuid)
    data: dict = field(default_factory=empty_dict)
    created_at: str = field(default_factory=current_iso_datetime)
    updated_at: str = field(default_factory=current_iso_datetime)

    def to_dict(self) -> dict:
        return asdict(self, dict_factory=dict)
