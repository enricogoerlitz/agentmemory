import re

from datetime import datetime

from agentmemory.utils.dataclasses.default_factory_functions import current_iso_datetime, empty_dict, uuid


def test_current_iso_datetime():
    iso_str = current_iso_datetime()
    assert isinstance(iso_str, str)
    parsed = datetime.fromisoformat(iso_str)
    assert parsed.tzinfo is not None


def test_uuid():
    u = uuid()
    assert isinstance(u, str)
    assert len(u) == 32
    assert re.fullmatch(r"[0-9a-f]{32}", u)


def test_empty_dict():
    d = empty_dict()
    assert isinstance(d, dict)
    assert d == {}
    assert d is not empty_dict()  # check for new instance
