from enum import Enum

from agentmemory.connection.longterm.collections import Collection


class CacheRetrieveType(str, Enum):
    GET = "GET"
    LIST = "LIST"
    LIST_UNTIL_ID_FOUND = "LIST_UNTIL_ID_FOUND"

    def members(self) -> list[str]:
        return [member for member in self]


class ClearCacheTransactionType(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

    def members(self) -> list[str]:
        return [member for member in self]


def _create_rtype(rtype: CacheRetrieveType) -> str:
    if rtype not in CacheRetrieveType:
        raise ValueError(f"CacheRetrieveType value must be in '{CacheRetrieveType.members()}'")
    return f"type:{rtype.value}"


def _create_col(col: Collection) -> str:
    if col not in Collection:
        raise ValueError(f"Collection value must be in '{Collection.members()}'")
    return f"col:{col.value}"


def _create_id(id: str | tuple[str, str] = None, rtype: CacheRetrieveType = None) -> str | None:
    if id is None and rtype == CacheRetrieveType.GET:
        raise ValueError("If the CacheRetrieveType is equals 'GET', you need to pass in an id.")

    if id is None:
        return None

    if isinstance(id, str) and len(id) > 0:
        return f"id:{id}"

    if isinstance(id, tuple) and len(id) == 2:
        ids = ",".join([_id for _id in id])
        return f"id:{ids}"

    raise ValueError(f"id must be None, a string with a minimum length of 1 or a tuple with 2 entries, but was: {str(id)}")


def _create_query(query: dict = None) -> str | None:
    if query is None:
        return None

    if isinstance(query, dict):
        return f"q:{str(query)}"

    raise ValueError("Query must be None or an dict.")


def _create_kwargs(kwargs: dict) -> str | None:
    if len(kwargs.keys()) == 0:
        return None

    kwargs_ = ";".join([f"{k}:{v}" for k, v in kwargs.items()])
    return kwargs_


class CacheKey:
    def __init__(
            self,
            *,
            rtype: CacheRetrieveType,
            col: Collection,
            id: str | tuple[str, str] = None,
            query: dict = None,
            **kwargs
    ):
        self._rtype = _create_rtype(rtype)
        self._col = _create_col(col)
        self._id = _create_id(id, rtype)
        self._q = _create_query(query)
        self._kwargs = _create_kwargs(kwargs)

    def key(self) -> str:
        keys = [self._rtype, self._col, self._id, self._q, self._kwargs]
        key = ";".join([key for key in keys if key is not None])
        return key

    def __str__(self):
        return self.key()


class ClearCacheKey:
    def __init__(
            self,
            *,
            ttype: ClearCacheTransactionType,
            col: Collection,
            id: str | tuple[str, str] = None,
            is_first_id_anchor: bool = False
    ):
        self._ttype = ttype
        self._col = col
        self._id = id
        self._is_first_id_anchor = is_first_id_anchor

    def clear_keys(self) -> list[str]:
        """
        CREATE:
            - clear rtype:LIST; exception: first_id_is_anchor -> rtype:LIST and ID=...*
            - don't clear rtype:GET
        UPDATE:
            - clear rtype:LIST; exception: first_id_is_anchor -> rtype:LIST and ID=...*
            - clear rtype:GET by ID
        DELETE:
            - clear rtype:LIST; exception: first_id_is_anchor -> rtype:LIST and ID=...*
            - clear rtype:GET by ID
        """
        if self._ttype not in ClearCacheTransactionType:
            raise ValueError(f"ClearCacheTransactionType value must be in '{ClearCacheTransactionType.members()}'")

        rgettype = _create_rtype(CacheRetrieveType.GET)
        rlisttype = _create_rtype(CacheRetrieveType.LIST)
        id = _create_id(self._id, "?")
        col = _create_col(self._col)

        clear_list_key = f"{rlisttype};{col}*"
        if self._is_first_id_anchor:
            if not isinstance(self._id, tuple) or len(self._id) != 2:
                raise ValueError("If 'is_first_id_anchor=True', the id must be a tuple with 2 entries.")
            clear_list_key = f"{rlisttype};{col};id:{self._id[0]}*"

        if self._ttype == ClearCacheTransactionType.CREATE:
            return [clear_list_key]

        id = _create_id(self._id, CacheRetrieveType.GET)
        clear_get_key = f"{rgettype};{col};{id}*"

        return [clear_get_key, clear_list_key]

    def __str__(self):
        return str(self.clear_keys())
