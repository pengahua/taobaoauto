from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.integrations.taobao.client import TopClient
from app.integrations.taobao.orders import TaobaoOrderAdapter
from app.models.api_call_log import ApiCallLog  # noqa: F401
from app.models.audit_log import AuditLog  # noqa: F401
from app.models.command import CommandRecord  # noqa: F401
from app.models.exception_task import ExceptionTaskRecord  # noqa: F401
from app.models.kill_switch import KillSwitchRecord  # noqa: F401
from app.models.order import Order, OrderStatusHistory  # noqa: F401
from app.models.store import Store  # noqa: F401
from app.services.platform_api_proxy import PlatformApiProxy


def make_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()


def test_order_adapter_prepares_signed_request() -> None:
    adapter = TaobaoOrderAdapter(TopClient(app_key="app", app_secret="secret"))

    prepared = adapter.prepare_order_detail_request(session_key="session", tid="123")

    assert prepared.signed_params["method"] == "taobao.trade.fullinfo.get"
    assert prepared.signed_params["session"] == "session"
    assert prepared.signed_params["tid"] == "123"
    assert "sign" in prepared.signed_params


def test_platform_api_proxy_records_prepared_request() -> None:
    db = make_session()
    adapter = TaobaoOrderAdapter(TopClient(app_key="app", app_secret="secret"))
    prepared = adapter.prepare_sold_orders_request(
        session_key="session",
        start_modified="2026-06-08 00:00:00",
        end_modified="2026-06-08 23:59:59",
    )

    PlatformApiProxy(db).record_prepared_request(
        store_id="s1",
        api_name="taobao.trades.sold.get",
        prepared=prepared,
    )
    db.commit()

    records = db.query(ApiCallLog).all()
    assert len(records) == 1
    assert records[0].api_name == "taobao.trades.sold.get"
    assert records[0].response_code == "prepared"

