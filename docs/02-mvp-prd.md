# MVP PRD v0.1

## 1. Objective

Deliver a read-safe, audit-first MVP that lets a merchant connect a Taobao shop, synchronize orders, inspect fulfillment readiness, draft AI customer replies, and manage exceptions.

The MVP must prove the platform architecture without allowing high-risk autonomous actions.

## 2. In Scope

| Module | MVP Capability |
|---|---|
| Shop authorization | Generate authorization URL, store authorization state, display permission diagnostics |
| Order sync | Import paid and pending-shipment orders, show order status, keep status history |
| Order workbench | Filter by status, risk level, fulfillment readiness, exception reason |
| Customer service assist | Draft replies using buyer message plus verified order facts; no auto-send by default |
| Waybill visibility | Create waybill command placeholder, show print/shipment task state |
| Exception queue | Show orders blocked by refund, missing SKU mapping, missing facts, API failure, or policy hold |
| Rule policy | Evaluate whether an action is allowed, held, or requires human approval |
| Audit | Record AI runs, policy decisions, commands, and future external API calls |

## 3. Out of Scope

- Automatic refund approval or refusal
- Automatic address change
- Automatic compensation
- Automatic trade close
- Complex split/merge orders
- Multi-warehouse routing
- Unofficial scraping or browser automation

## 4. Primary Users

| User | Needs |
|---|---|
| Store owner | See automation rate, risk holds, and business impact |
| Operations manager | Configure low-risk rules and inspect stuck orders |
| Customer service | Get accurate draft replies with order context |
| Warehouse operator | See waybill and shipment task status |
| Auditor | Replay automated decisions and sensitive actions |

## 5. Core User Stories

1. As an admin, I can start Taobao shop authorization and see whether permissions are available.
2. As an operator, I can view synchronized orders and understand why an order can or cannot be automated.
3. As customer service, I can paste or receive a buyer message and get a safe reply draft.
4. As operations, I can evaluate a proposed action against policy before execution.
5. As an auditor, I can review commands, AI outputs, policy decisions, and future API calls by trace id.

## 6. Acceptance Criteria

| Area | Criteria |
|---|---|
| Safety | High-risk actions return `human_required=true` |
| AI | Reply drafts are not auto-send by default until RAG and policy checks are connected |
| Idempotency | Write commands require an idempotency key |
| Audit | Every policy decision and command can be represented as an audit event |
| UI | Console shows shop, order, customer service, fulfillment, risk, and audit entry points |
| Reliability | Health endpoint works and code builds locally |

