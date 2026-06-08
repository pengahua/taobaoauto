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

