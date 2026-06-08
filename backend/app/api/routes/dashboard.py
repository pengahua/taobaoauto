from fastapi import APIRouter

from app.schemas.dashboard import DashboardMetric, DashboardSummary

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary() -> DashboardSummary:
    return DashboardSummary(
        service_status="ok",
        automation_boundary="L0-L1",
        mvp_focus="订单到履约",
        risk_policy="高风险动作人审强制",
        audit_policy="全链路回放",
        metrics=[
            DashboardMetric(label="自动化边界", value="L0-L1", status="active"),
            DashboardMetric(label="MVP 重点", value="订单到履约", status="active"),
            DashboardMetric(label="高风险动作", value="人审强制", status="blocked"),
            DashboardMetric(label="审计要求", value="全链路回放", status="active"),
        ],
    )

