export type DashboardMetric = {
  label: string;
  value: string;
  status: string;
};

export type DashboardSummary = {
  service_status: string;
  automation_boundary: string;
  mvp_focus: string;
  risk_policy: string;
  audit_policy: string;
  metrics: DashboardMetric[];
};

export type PolicyDecision = {
  decision: string;
  human_required: boolean;
  reasons: string[];
};

export type ExceptionTask = {
  id: string;
  type: string;
  title: string;
  severity: string;
  owner_role: string;
  next_action: string;
};

export type ExceptionTaskList = {
  items: ExceptionTask[];
};

export type KillSwitchState = {
  store_id: string;
  global_pause: boolean;
  customer_message_pause: boolean;
  waybill_pause: boolean;
  shipment_pause: boolean;
  refund_pause: boolean;
};

export type AutoReplyRequest = {
  store_id: string;
  thread_id: string;
  buyer_message: string;
  order_tid?: string;
  verified_facts?: Record<string, string>;
  allow_auto_send?: boolean;
  conversation_history?: string[];
};

export type AutoReplyResponse = {
  draft: string;
  risk_level: string;
  auto_send_allowed: boolean;
  required_facts: string[];
  escalation_reason: string | null;
  provider: string;
  model: string;
  redacted: boolean;
  intent: string;
  decision: string;
  next_action: string;
};

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API ${path} failed with ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function getDashboardSummary(): Promise<DashboardSummary> {
  return request<DashboardSummary>("/dashboard/summary");
}

export function evaluateShipmentPolicy(): Promise<PolicyDecision> {
  return request<PolicyDecision>("/policy/evaluate", {
    method: "POST",
    body: JSON.stringify({
      store_id: "demo-store",
      scene: "shipment",
      action: "mark_order_shipped",
      risk_level: "L1",
      has_verified_facts: true,
    }),
  });
}

export function getExceptionTasks(): Promise<ExceptionTaskList> {
  return request<ExceptionTaskList>("/tasks/exceptions");
}

export function getKillSwitches(): Promise<KillSwitchState> {
  return request<KillSwitchState>("/risk/kill-switches");
}

export function createAutoReply(payload: AutoReplyRequest): Promise<AutoReplyResponse> {
  return request<AutoReplyResponse>("/ai/customer-auto-reply", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
