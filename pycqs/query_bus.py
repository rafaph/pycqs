"""This module provides the QueryBus class for executing queries."""

from abc import ABC, abstractmethod
from collections.abc import Awaitable
from typing import Generic, TypeVar, cast

T = TypeVar('T', bound='Query')
R = TypeVar('R', bound='QueryResult')


class Query:
    """Represents a query."""


class QueryResult:
    """Represents the result of a query."""


class QueryHandler(ABC, Generic[T, R]):
    """Represents a query handler."""

    @abstractmethod
    def execute(self, query: T) -> Awaitable[R]:
        """Executes a query and returns the result asynchronously."""
        raise NotImplementedError


class QueryBus:
    """Represents a query bus for executing queries."""

    def __init__(self) -> None:
        self._queries: dict[
            type[Query],
            QueryHandler[Query, QueryResult],
        ] = {}

    def register_handler(
        self,
        query: type[T],
        handler: QueryHandler[T, R],
    ) -> None:
        """Register a query handler.

        Args:
            query (type[T]): The type of query to handle.
            handler (QueryHandler[T]): The query handler.
        """
        self._queries[query] = cast(
            QueryHandler[Query, QueryResult],
            handler,
        )

    async def execute(self, query: T) -> R:
        """Executes a query and returns the result asynchronously."""
        class_type = query.__class__

        if class_type not in self._queries:
            msg = f'No query handler defined for {class_type.__name__}'
            raise ValueError(msg)

        handler = cast(QueryHandler[T, R], self._queries[class_type])

        return await handler.execute(query)
