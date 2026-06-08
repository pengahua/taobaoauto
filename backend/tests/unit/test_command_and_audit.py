from app.audit.service import AuditEvent, AuditService, InMemoryAuditSink
from app.commands.bus import CommandBus
from app.commands.idempotent_executor import IdempotentExecutor
from app.domain.commands import Command


def test_command_bus_dispatches_registered_handler() -> None:
    bus = CommandBus()
    command = Command(
        command_type="demo",
        store_id="s1",
        biz_key="tid-1",
        idempotency_key="demo:s1:tid-1",
        payload={"ok": True},
    )

    bus.register("demo", lambda cmd: {"biz_key": cmd.biz_key})

    assert bus.dispatch(command) == {"biz_key": "tid-1"}


def test_idempotent_executor_returns_existing_record() -> None:
    executor = IdempotentExecutor()
    command = Command(
        command_type="grant_entitlement",
        store_id="s1",
        biz_key="oid-1",
        idempotency_key="entitlement:s1:oid-1:vip",
        payload={},
    )

    first = executor.execute(command, lambda _: {"attempt": 1})
    second = executor.execute(command, lambda _: {"attempt": 2})

    assert first.result == {"attempt": 1}
    assert second.result == {"attempt": 1}


def test_audit_service_appends_event() -> None:
    sink = InMemoryAuditSink()
    service = AuditService(sink=sink)

    service.record(
        AuditEvent(
            actor_type="system",
            action="policy.evaluate",
            target_type="order",
            target_id="tid-1",
            store_id="s1",
            trace_id="trace-1",
            metadata={"decision": "hold"},
        )
    )

    assert len(sink.events) == 1
    assert sink.events[0].metadata["decision"] == "hold"

