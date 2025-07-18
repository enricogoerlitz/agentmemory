from typing import Type


class AgentMemoryError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ObjectNotFoundError(AgentMemoryError):
    def __init__(self, collection: str, id: str | tuple[str]):
        id = str(id)
        msg = f"Object with ID '{id}' not found in collection '{collection}'."
        super().__init__(msg)


class ObjectNotUpdatedError(AgentMemoryError):
    def __init__(self, collection: str, id: str | tuple[str]):
        id = str(id)
        msg = f"Object with ID '{id}' in collection '{collection}' could not be updated."
        super().__init__(msg)


class ObjectNotDeletedError(AgentMemoryError):
    def __init__(self, collection: str, id: str | tuple[str], e: Exception):
        id = str(id)
        msg = f"Object with ID '{id}' in collection '{collection}' could not be deleted because: {e}."
        super().__init__(msg)


class ObjectNotCreatedError(AgentMemoryError):
    def __init__(self, msg: str = None, e: Exception = None):
        msg = msg or f"Object could not be created because: {e}"
        super().__init__(msg)


class InstanceTypeError(AgentMemoryError):
    def __init__(self, obj: object, cls: Type):
        obj_name = str(type(obj))
        cls_name = str(type(cls))
        msg = f"Unexpected type: Given is a object of type '{obj_name}', but expected is a object of type '{cls_name}'"
        super().__init__(msg)
