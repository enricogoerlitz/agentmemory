import pytest

from agentmemory import AgentMemory
from agentmemory.connection import AgentMemoryConnection
from agentmemory.connection.longterm import MongoDBConnection
from agentmemory.connection.shortterm import RedisConnection


@pytest.fixture(scope="session")
def pymongo_memory() -> AgentMemory:
    con = AgentMemoryConnection(
        longterm_con=MongoDBConnection(
            mongo_uri="mongodb://localhost:27017",
            database="test-agentmemory-pymongo"
        ),
        shortterm_con=None
    )
    memory = AgentMemory("test-agent", con=con)
    return memory


@pytest.fixture(scope="session")
def pymongo_cache_memory() -> AgentMemory:
    con = AgentMemoryConnection(
        longterm_con=MongoDBConnection(
            mongo_uri="mongodb://localhost:27017",
            database="test-cache-agentmemory-pymongo-redis"
        ),
        shortterm_con=RedisConnection(
            host="localhost"
        )
    )
    memory = AgentMemory("test-cache-agent", con=con)
    return memory
