from pydantic import BaseModel


class DashboardMetric(BaseModel):
    label: str
    value: str
    status: str


class DashboardSummary(BaseModel):
    service_status: str
    automation_boundary: str
    mvp_focus: str
    risk_policy: str
    audit_policy: str
    metrics: list[DashboardMetric]

