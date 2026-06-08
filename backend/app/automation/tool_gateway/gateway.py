from app.audit.service import AuditEvent, AuditService
from app.automation.tool_gateway.registry import ToolRegistry
from app.services.tool_gateway import ToolRequest


class AuditedToolGateway:
    def __init__(self, registry: ToolRegistry, audit: AuditService) -> None:
        self.registry = registry
        self.audit = audit

    def execute(self, request: ToolRequest, trace_id: str) -> dict:
        handler = self.registry.get(request.tool_name)
        result = handler(request.payload)
        self.audit.record(
            AuditEvent(
                actor_type="ai_agent",
                action=f"tool.{request.tool_name}",
                target_type="tool",
                target_id=request.tool_name,
                store_id=request.store_id,
                trace_id=trace_id,
                metadata={
                    "risk_level": request.risk_level,
                    "idempotency_key": request.idempotency_key,
                    "result_status": result.get("status", "unknown"),
                },
            )
        )
        return result

