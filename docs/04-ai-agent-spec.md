# AI Agent Specification v0.1

## 1. Core Principle

The LLM is not the business owner. It is an understanding, generation, classification, and orchestration assistant.

Business state machines, policy rules, and human approvals own final execution.

## 2. Agent Roles

| Agent | Responsibility | Automation Boundary |
|---|---|---|
| Customer Service Agent | Intent detection, fact retrieval, reply drafting/sending | Auto only for low-risk scenarios |
| Order Agent | Validate payment, status, SKU, refund state, hold state | Mostly automatic |
| Entitlement Agent | Create account and grant entitlement | Automatic if paid, mapped, and idempotent |
| Waybill Agent | Create waybill and print task | Automatic after order validation |
| Shipment Agent | Mark order shipped | Automatic only after waybill and state checks |
| After-sales Agent | Classify and summarize refund/return/reissue cases | Recommendation first |
| Risk Agent | Detect abnormal buyer/order/refund patterns | Advisory and blocking |
| QA Agent | Audit automated replies and actions | Async and sampled |
| Human Collaboration Agent | Summarize context and create manual tasks | Automatic |

## 3. Tool Gateway

LLM agents call internal tools through a Tool Gateway. They never call platform APIs directly.

Required checks:

- Permission
- Parameter schema validation
- Business state validation
- Idempotency key
- Risk level
- Audit log
- Rate limit

## 4. Knowledge Base

Knowledge categories:

- Product and SKU knowledge
- Presales scripts
- After-sales policies
- Operation SOPs
- Logistics rules
- Risk cases

Recommended structured knowledge record:

```json
{
  "title": "Virtual membership opening failure",
  "scope": "after_sales/entitlement",
  "applicable_sku": ["vip_monthly", "vip_yearly"],
  "conditions": [
    "order status is paid",
    "entitlement status is unopened",
    "buyer has not requested refund"
  ],
  "allowed_actions": ["create_account", "grant_entitlement", "send_qianniu_message"],
  "forbidden_actions": ["promise extra compensation", "manual refund"],
  "human_escalation": [
    "abnormal order amount",
    "same buyer repeated opening more than 2 times",
    "entitlement API failed more than once"
  ]
}
```

## 5. Automation Levels

| Level | Policy | Examples |
|---|---|---|
| L0 | Fully automatic | FAQ, order query, logistics query, resend instructions |
| L1 | Automatic with async QA | Standard waybill creation, shipment reminder |
| L2 | AI suggestion plus human confirmation | Address change, refund mismatch, repeated entitlement |
| L3 | Manual only | Complaint, large refund, legal/privacy dispute, platform intervention |

## 6. Anti-Hallucination Rules

- Order, logistics, entitlement, and refund states must come from tool results.
- Refund policies and shipping commitments must cite knowledge base records or configured rules.
- High-risk scripts must use approved templates.
- Tool calls must run precondition checks before execution.
- After writes, the system must query state again when feasible.
- Rule conflicts, low confidence, or missing facts always escalate to human.
- Every automated reply stores source message, retrieved facts, model output, final sent content, model version, and policy version.

## 7. Evaluation Metrics

| Category | Metric |
|---|---|
| Customer service | Intent accuracy, first-contact resolution, transfer rate, violation rate |
| Fulfillment | Missed order rate, duplicate account rate, duplicate shipment rate, waybill success |
| After-sales | Wrong refund rate, wrong refusal rate, platform intervention rate |
| Safety | Hallucination rate, blocked risky actions, policy conflict detection |
| Operations | Automation rate, manual handling time, API failure rate |

