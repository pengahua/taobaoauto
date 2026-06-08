from fastapi import APIRouter

from app.api.routes import ai, audit, dashboard, health, orders, policy, shops, tasks

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(shops.router, prefix="/shops", tags=["shops"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(policy.router, prefix="/policy", tags=["policy"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])
