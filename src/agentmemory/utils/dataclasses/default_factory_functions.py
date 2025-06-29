from datetime import datetime, timezone
from uuid import uuid4


def current_iso_datetime() -> str:
    """
    Returns the current date and time in ISO 8601 format.

    Returns:
        str: Current date and time in ISO 8601 format.
    """
    return datetime.now(timezone.utc).isoformat()


def uuid() -> str:
    """
    Generates a unique identifier.

    Returns:
        str: A unique identifier.
    """
    return uuid4().hex


def empty_dict() -> dict:
    return {}
