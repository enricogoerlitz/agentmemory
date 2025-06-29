from agentmemory.connection.longterm.interface import LongtermMemoryConnectionInterface
# from agentmemory.connection.shortterm.interface import ShorttermConnectionInterface


class AgentMemoryConnection:
    def __init__(
            self,
            longterm_con: LongtermMemoryConnectionInterface,
            shortterm_con: str = None
    ):
        self._longterm_con = longterm_con
        self._shortterm_con = shortterm_con

    @property
    def longterm(self) -> LongtermMemoryConnectionInterface:
        """
        Returns the long-term conversation connection string.

        Returns:
            str: Long-term conversation connection string.
        """
        return self._longterm_con

    @property
    def shortterm(self) -> str:
        """
        Returns the short-term conversation connection string.

        Returns:
            str: Short-term conversation connection string.
        """
        return self._shortterm_con
