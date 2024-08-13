"""This module provides the CommandBus class for executing commands."""

from abc import ABC, abstractmethod
from collections.abc import Awaitable
from typing import Generic, TypeVar, cast

T = TypeVar('T', bound='Command')


class Command:
    """Represents a command."""


class CommandHandler(ABC, Generic[T]):
    """Represents a command handler."""

    @abstractmethod
    def execute(self, command: T) -> Awaitable[None]:
        """Execute the command."""
        raise NotImplementedError


class CommandBus:
    """Represents a command bus for executing commands."""

    def __init__(self) -> None:
        self._commands: dict[type[Command], set[CommandHandler[Command]]] = {}

    def register_handler(
        self,
        command: type[T],
        handler: CommandHandler[T],
    ) -> None:
        """Register a command handler.

        Args:
            command (type[T]): The type of command to handle.
            handler (CommandHandler[T]): The command handler.
        """
        if command not in self._commands:
            self._commands[command] = set()

        typed_handler = cast(CommandHandler[Command], handler)

        self._commands[command].add(typed_handler)

    async def execute(self, command: T) -> None:
        """Execute the command asynchronously.

        Args:
            command (T): The command to execute.

        Returns:
            None
        """
        class_type = command.__class__

        if class_type not in self._commands:
            msg = f'No command handler defined for {class_type.__name__}'
            raise ValueError(msg)

        handlers = self._commands[class_type]

        for handler in handlers:
            await handler.execute(command)
