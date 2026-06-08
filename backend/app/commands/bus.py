from collections.abc import Callable

from app.domain.commands import Command

CommandHandler = Callable[[Command], dict]


class CommandBus:
    def __init__(self) -> None:
        self._handlers: dict[str, CommandHandler] = {}

    def register(self, command_type: str, handler: CommandHandler) -> None:
        self._handlers[command_type] = handler

    def dispatch(self, command: Command) -> dict:
        handler = self._handlers.get(command.command_type)
        if handler is None:
            raise LookupError(f"No handler registered for command type: {command.command_type}")
        return handler(command)

