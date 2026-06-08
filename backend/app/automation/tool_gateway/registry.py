from collections.abc import Callable

ToolHandler = Callable[[dict], dict]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolHandler] = {}

    def register(self, name: str, handler: ToolHandler) -> None:
        self._tools[name] = handler

    def get(self, name: str) -> ToolHandler:
        handler = self._tools.get(name)
        if handler is None:
            raise LookupError(f"Tool is not registered: {name}")
        return handler

