import { useEffect, useMemo, useState } from "react";
import {
  Bot,
  ClipboardList,
  FileText,
  KeyRound,
  PackageCheck,
  ShieldCheck,
  Truck,
} from "lucide-react";
import {
  DashboardSummary,
  PolicyDecision,
  evaluateShipmentPolicy,
  getDashboardSummary,
} from "./lib/api";

const sections = [
  {
    title: "店铺授权",
    description: "OAuth、SessionKey、权限诊断和多店铺隔离。",
    icon: KeyRound,
    status: "Sprint 1",
  },
  {
    title: "订单工作台",
    description: "订单同步、状态机、异常标记、履约入口。",
    icon: ClipboardList,
    status: "Sprint 2",
  },
  {
    title: "客服会话",
    description: "AI 草稿、订单事实查询、低风险自动回复。",
    icon: Bot,
    status: "Sprint 3",
  },
  {
    title: "打单发货",
    description: "菜鸟面单、打印任务、发货回传和补偿查询。",
    icon: Truck,
    status: "Sprint 2",
  },
  {
    title: "权益开户",
    description: "SKU 映射、账号创建、权益发放、买家通知。",
    icon: PackageCheck,
    status: "Sprint 3",
  },
  {
    title: "规则风控",
    description: "自动化边界、审批、熔断、售后风险阈值。",
    icon: ShieldCheck,
    status: "Sprint 4",
  },
  {
    title: "审计追踪",
    description: "AI、API、命令、审批和敏感数据访问全链路回放。",
    icon: FileText,
    status: "MVP 必备",
  },
];

const fallbackSummary: DashboardSummary = {
  service_status: "offline",
  automation_boundary: "L0-L1",
  mvp_focus: "订单到履约",
  risk_policy: "高风险动作人审强制",
  audit_policy: "全链路回放",
  metrics: [
    { label: "自动化边界", value: "L0-L1", status: "active" },
    { label: "MVP 重点", value: "订单到履约", status: "active" },
    { label: "高风险动作", value: "人审强制", status: "blocked" },
    { label: "审计要求", value: "全链路回放", status: "active" },
  ],
};

export function App() {
  const [summary, setSummary] = useState<DashboardSummary>(fallbackSummary);
  const [policy, setPolicy] = useState<PolicyDecision | null>(null);
  const [apiError, setApiError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    Promise.all([getDashboardSummary(), evaluateShipmentPolicy()])
      .then(([dashboard, decision]) => {
        if (!mounted) return;
        setSummary(dashboard);
        setPolicy(decision);
        setApiError(null);
      })
      .catch((error: Error) => {
        if (!mounted) return;
        setApiError(error.message);
      });

    return () => {
      mounted = false;
    };
  }, []);

  const apiStatus = useMemo(() => {
    if (apiError) return "API 离线";
    return summary.service_status === "ok" ? "API 在线" : "只读试运行";
  }, [apiError, summary.service_status]);

  return (
    <main className="shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brandMark">TA</span>
          <div>
            <strong>Autopilot</strong>
            <span>Commerce Console</span>
          </div>
        </div>
        <nav>
          {sections.map((section) => (
            <a href="#" key={section.title}>
              <section.icon size={18} />
              {section.title}
            </a>
          ))}
        </nav>
      </aside>

      <section className="content">
        <header className="topbar">
          <div>
            <p>项目中台</p>
            <h1>淘宝无人值守电商链路</h1>
          </div>
          <button type="button">{apiStatus}</button>
        </header>

        <section className="metrics">
          {summary.metrics.map((metric) => (
            <div key={metric.label}>
              <span>{metric.label}</span>
              <strong>{metric.value}</strong>
            </div>
          ))}
        </section>

        <section className="controlBand">
          <div>
            <span>策略引擎</span>
            <strong>{policy?.decision === "allow" ? "发货策略通过" : "等待策略结果"}</strong>
            <p>
              {policy
                ? policy.reasons.join("；")
                : "正在检查 mark_order_shipped 的默认自动化边界。"}
            </p>
          </div>
          <div>
            <span>风险策略</span>
            <strong>{summary.risk_policy}</strong>
            <p>{summary.audit_policy}</p>
          </div>
        </section>

        <section className="grid">
          {sections.map((section) => (
            <article key={section.title} className="card">
              <div className="cardIcon">
                <section.icon size={22} />
              </div>
              <div>
                <h2>{section.title}</h2>
                <p>{section.description}</p>
                <span>{section.status}</span>
              </div>
            </article>
          ))}
        </section>
      </section>
    </main>
  );
}

