from fastapi import APIRouter

from app.schemas.tasks import ExceptionTask, ExceptionTaskList

router = APIRouter()


@router.get("/exceptions", response_model=ExceptionTaskList)
def list_exception_tasks() -> ExceptionTaskList:
    return ExceptionTaskList(
        items=[
            ExceptionTask(
                id="perm-qn-msg",
                type="missing_permission",
                title="确认千牛消息接口权限",
                severity="high",
                owner_role="Taobao Integration",
                next_action="在开放平台控制台核验千牛消息读写能力",
            ),
            ExceptionTask(
                id="risk-refund-auto",
                type="policy_hold",
                title="退款自动化保持关闭",
                severity="critical",
                owner_role="Risk Lead",
                next_action="只允许售后建议和人工确认，不开放自动同意/拒绝退款",
            ),
        ]
    )


@router.get("/commands")
def list_commands() -> dict[str, list[dict[str, str]]]:
    return {"items": []}
