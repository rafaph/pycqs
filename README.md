# pycqs

Command Query Segregation (CQS) utilities for Python.

Provides the `CommandBus` and `QueryBus` classes.

## Requirements

Python 3.10 or above.

## Installation

You can use `pip` to install pycqs with e.g.:

```sh
pip install pycqs
```

## Usage

- Using the `CommandBus`.

```python
import asyncio
from dataclasses import dataclass

from pycqs import (
    Command,
    CommandBus,
    CommandHandler,
)


# Create the command
@dataclass
class HelloWorldCommand(Command):
    name: str


# Create the command handler
class HelloWorldCommandHandler(
    CommandHandler[HelloWorldCommand],
):
    async def execute(
        self,
        command: HelloWorldCommand,
    ) -> None:
        print(f'Hello World, {command.name}')


async def main() -> None:
    # Initialize the command bus
    command_bus = CommandBus()
    command_bus.register_handler(
        HelloWorldCommand,
        HelloWorldCommandHandler(),
    )

    # Execute a command
    command = HelloWorldCommand('cqs')
    await command_bus.execute(command)


if __name__ == '__main__':
    asyncio.run(main())
```

More usage examples on [tests](./tests/test_command_bus.py).

- Using the `QueryBus`.

```python
import asyncio
from dataclasses import dataclass

from pycqs import (
    Query,
    QueryBus,
    QueryHandler,
    QueryResult,
)


# Create the query
@dataclass
class HelloWorldQuery(Query):
    name: str


# Create the query result
@dataclass
class HelloWorldQueryResult(QueryResult):
    message: str


# Create the query handler
class HelloWorldQueryHandler(
    QueryHandler[
        HelloWorldQuery,
        HelloWorldQueryResult,
    ],
):
    async def execute(
        self,
        query: HelloWorldQuery,
    ) -> HelloWorldQueryResult:
        message = f'Hello World, {query.name}'
        return HelloWorldQueryResult(message)


async def main() -> None:
    # Initialize the query bus
    query_bus = QueryBus()
    query_bus.register_handler(
        HelloWorldQuery,
        HelloWorldQueryHandler(),
    )

    # Execute a query
    query = HelloWorldQuery('cqs')
    query_result: HelloWorldQueryResult = await query_bus.execute(query)
    print(query_result.message)


if __name__ == '__main__':
    asyncio.run(main())
```

More usage examples on [tests](./tests/test_query_bus.py).

## License

MIT
