from typing import Iterator

from agentmemory.schema.personas import Persona
from agentmemory.connection.connection import AgentMemoryConnection
from agentmemory.utils.dataclasses.default_factory_functions import current_iso_datetime
from agentmemory.utils.validation.instance import check_isinstance


# TODO:
# - implement caching for get, list, create, update, delete methods
# - clear cache when persona is created, updated or deleted

class Personas:
    def __init__(self, con: AgentMemoryConnection):
        self._con = con
        self._personas = con.longterm.personas()

    def get(self, persona_id: str, cache_cnf: dict = None) -> Persona:
        return self._personas.get(persona_id)

    def get_by_name(self, name: str, cache_cnf: dict = None) -> Persona:
        return self._personas.get_by_name(name)

    def list(self, query: dict = None, cache_cnf: dict = None) -> Iterator[Persona]:
        return self._personas.list(query)

    def create(self, persona: Persona) -> Persona:
        check_isinstance(persona, Persona)
        return self._personas.create(persona)

    def update(self, persona: Persona) -> Persona:
        check_isinstance(persona, Persona)
        persona.updated_at = current_iso_datetime()
        update_data = {
            "name": persona.name,
            "role": persona.role,
            "goals": persona.goals,
            "background": persona.background,
            "embedding": persona.embedding,
            "updated_at": persona.updated_at
        }
        return self._personas.update(persona.persona_id, update_data)

    def delete(self, persona_id: str) -> None:
        return self._personas.delete(persona_id)
