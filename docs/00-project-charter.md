# Taobao Autopilot Commerce - Project Charter v0.1

## 1. Project Goal

Build a production-grade Taobao/Tmall commerce automation platform based on Taobao Open Platform, Qianniu, Cainiao electronic waybill APIs, and LLM agents.

The platform should gradually automate:

- Customer service
- Order synchronization
- Automatic account creation / entitlement granting
- Waybill creation and printing
- Shipment confirmation
- After-sales triage
- Risk control and audit

The system must not be a blind "fully autonomous bot". Business state machines and rule engines own final execution decisions. LLM agents provide understanding, classification, response generation, and action suggestions.

## 2. Operating Principles

1. Deterministic business logic first, AI second.
2. All write actions must be guarded by rules, permissions, idempotency, and audit logs.
3. Refund, compensation, address changes, repeat entitlement grants, and high-risk after-sales actions require human confirmation until enough production evidence exists.
4. Customer service agents can speak more, but execute less. Fulfillment agents speak less, but execute only with strict validation.
5. Every automated action must be explainable and replayable.
6. Start with low-risk repeatable workflows, then expand automation boundaries by scenario.

## 3. Virtual Team

| Team | Responsibility | Current Lead |
|---|---|---|
| PMO / Chief Architect | Program control, architecture decisions, task decomposition, final integration | Codex |
| Product & Business Architecture | Business domains, SOPs, role journeys, MVP/V1/V2 scope | Product Agent |
| Taobao Integration | OAuth, TOP APIs, Qianniu APIs, Cainiao APIs, permission matrix | Integration Agent |
| Backend Platform | Domain services, database, queues, idempotency, observability | Backend Agent |
| AI Agent Platform | Agent design, tool calling, RAG, evaluation, anti-hallucination | AI Agent |
| Security & Risk | Privacy, platform rules, refund boundaries, audit, RBAC | Risk Agent |
| Frontend Console | Operations dashboard, exception queues, approvals, configuration | Frontend Team |
| QA & SRE | Sandbox testing, regression, monitoring, incident drills | QA/SRE Team |

## 4. Business Domains

| Domain | Core Responsibility | MVP Boundary |
|---|---|---|
| Shop Authorization | Shop OAuth, token storage, permission diagnostics | Single or small number of shops |
| Product & Entitlement | SKU mapping, entitlement package, account opening rules | Standard SKU to one entitlement type |
| Customer Service | Message intake, intent detection, reply suggestions, human takeover | FAQ, order status, logistics query |
| Order Sync | Initial and incremental order synchronization | Paid and pending-shipment orders |
| Fulfillment Orchestration | Convert orders into executable tasks | One order one fulfillment task |
| Account / Entitlement Opening | Create account, grant entitlement, notify buyer | One entitlement provider |
| Waybill & Printing | Cainiao waybill number, template, print task | Main carrier and one template |
| Shipment | Bind tracking number and mark shipped | Automatic callback for verified orders |
| After-sales | Refund/return sync, triage, suggested handling | Assist only; high risk stays manual |
| AI Decisioning | Intent, RAG answer, tool orchestration, risk summary | Suggestion plus low-risk automation |
| Rules & Risk | Automation boundaries, thresholds, blacklist, audit | Mandatory from MVP |
| Operations Console | Orders, conversations, exceptions, logs, rules | Required for MVP |
| Data & Audit | API logs, AI logs, task logs, metrics | Required for MVP |

## 5. AI Agent Roles

| Agent | Responsibility | Automation Level |
|---|---|---|
| Customer Service Agent | Understand buyer intent, retrieve facts, draft or send approved replies | High for low-risk FAQ |
| Order Agent | Validate order status, SKU, payment, refund state, hold state | High |
| Account Opening Agent | Create account and grant entitlement after payment | Medium-high |
| Waybill & Shipment Agent | Create waybill, print, and mark shipped after validation | Medium |
| After-sales Agent | Classify refund/return/reissue/compensation requests | Low at first |
| Risk Agent | Detect abnormal buyers, repeated refunds, sensitive promises | Medium |
| QA Agent | Audit replies and automated actions | High |
| Human Collaboration Agent | Summarize complex cases into work orders | High |

## 6. Tool Calling Rules

LLM agents never call Taobao, Qianniu, Cainiao, or internal entitlement APIs directly.

All calls go through a Tool Gateway:

```text
LLM Function Calling
        |
Tool Gateway
        |
Permission check + parameter validation + idempotency key + audit log
        |
API Adapter / Internal Service
```

Required internal tools:

| Tool | Type | Risk |
|---|---|---|
| get_order_detail | Read | Low |
| search_buyer_orders | Read | Low |
| get_logistics_status | Read | Low |
| send_qianniu_message | Write | Medium |
| create_account | Write | Medium |
| grant_entitlement | Write | Medium |
| create_waybill | Write | Medium |
| mark_order_shipped | Write | Medium-high |
| create_after_sale_ticket | Write | Medium |
| approve_refund | Write | High |
| escalate_to_human | Write | Low |

Every write tool must require an `idempotency_key`, structured input, structured output, and audit record.

## 7. Automation Risk Levels

| Level | Policy | Examples |
|---|---|---|
| L0 | Fully automatic | FAQ, order query, logistics query, resend instructions |
| L1 | Automatic with async QA | Standard waybill generation, shipment reminder, low-risk print retry |
| L2 | AI suggestion plus human confirmation | Address change, refund mismatch, repeated entitlement grant |
| L3 | Manual only | Complaint, platform intervention, legal/privacy dispute, large refund, low confidence |

## 8. Delivery Roadmap

### MVP

Goal: Run the basic "order sync + customer service assist + waybill/shipment visibility" loop.

Scope:

- Shop authorization
- Order sync and order state machine
- Customer service AI suggestions
- Logistics/order lookup
- Waybill task prototype
- Exception queue
- Audit logs
- Basic operations console

Acceptance targets:

- Order sync accuracy >= 99%
- Pending-shipment sync delay <= 5 minutes
- Standard waybill task success >= 95%
- FAQ hit rate >= 50%
- Repeated fulfillment caused by duplicate events = 0
- Refund-in-progress orders never auto-ship

### V1

Goal: Standard orders can be fulfilled automatically within configured rules.

Scope:

- Multi-shop support
- SKU / entitlement mapping
- Automatic account creation and entitlement grant
- Physical and virtual order routing
- Rule engine
- Unified task queue
- Monitoring and alerts
- After-sales assist

Acceptance targets:

- Standard order auto-fulfillment >= 70%
- Entitlement grant success >= 95%
- Customer service auto-resolution >= 40%
- Shipping timeliness >= 98%
- AI policy violation rate <= 0.5%

### V2

Goal: Near-unattended operation for standard business scenarios, with human supervision for exceptions.

Scope:

- Multi-warehouse, multi-carrier, split/merge order strategy
- Low-risk after-sales automation
- AI QA and risk prediction
- Proactive customer care
- Cost accounting
- Strategy gray release and rollback

Acceptance targets:

- Standard scenario no-human-intervention rate >= 85%
- Low-risk after-sales auto-processing >= 50%
- Human transfer rate <= 25%
- Wrong refund rate = 0
- All AI decisions are traceable and replayable

## 9. Immediate Next Work Packages

| ID | Work Package | Owner | Output |
|---|---|---|---|
| WP-001 | API capability and permission matrix | Taobao Integration | `docs/01-api-matrix.md` |
| WP-002 | Domain data model | Backend Platform | `docs/02-data-model.md` |
| WP-003 | Event and task architecture | Backend Platform | `docs/03-event-architecture.md` |
| WP-004 | AI agent and tool gateway spec | AI Agent Platform | `docs/04-ai-agent-spec.md` |
| WP-005 | Risk policy and approval matrix | Security & Risk | `docs/05-risk-policy.md` |
| WP-006 | MVP operations console IA | Frontend Console | `docs/06-console-ia.md` |
| WP-007 | 12-week execution plan | PMO | `docs/07-12-week-plan.md` |

