# Autonomous Operating Model v0.1

This project runs as a virtual software company. Each role owns a distinct review surface, and no feature is considered complete until it passes the cross-role loop.

## 1. Virtual Roles

| Role | Owns | Blocks Delivery When |
|---|---|---|
| Product Owner | PRD, scope, acceptance criteria | User workflow is unclear or MVP scope expands without review |
| Backend Lead | APIs, persistence, commands, integrations | Writes bypass command/audit/idempotency |
| AI Lead | Agents, tool calling, RAG, evaluation | Model can execute high-risk actions without policy checks |
| Risk Lead | Privacy, refund boundaries, RBAC, kill switches | Sensitive data, refund, compensation, address change, or shipment lacks audit |
| Frontend Lead | Console workflows and operator experience | Operators cannot see status, risk reason, or next action |
| QA Lead | Tests, smoke scripts, release gate | Unit tests, frontend build, API smoke, or browser smoke fails |
| SRE Lead | Local/dev/prod runbooks, monitoring, rollback | Service cannot be started, checked, or rolled back reliably |

## 2. Cross-Role Loop

Every iteration follows the same loop:

```text
Product defines acceptance
  -> Backend creates safe capability
  -> AI integrates only through Tool Gateway
  -> Risk verifies policy and audit
  -> Frontend exposes operator workflow
  -> QA runs automated gates
  -> SRE confirms runbook and observability
  -> Commit and push
```

If any role blocks, the iteration must either fix the blocker or explicitly document the degraded scope.

## 3. Quality Gates

Required before commit:

- Backend tests pass.
- Frontend build passes.
- Backend health endpoint returns 200.
- Dashboard endpoint returns 200.
- Browser smoke confirms API status, policy status, and audit navigation.
- High-risk actions remain human-gated.

Required before production:

- OAuth permissions verified.
- External API adapter contract tests pass.
- Data masking verified.
- Kill switches verified.
- Retry/idempotency tests pass for all write commands.
- Audit replay works for AI, command, and API decisions.

## 4. Autonomous Backlog Rules

The system prioritizes work in this order:

1. Safety foundations: audit, idempotency, policy, kill switch.
2. Deterministic commerce flow: auth, orders, SKU mapping, waybill, shipment.
3. Operator visibility: dashboard, exception queue, audit replay.
4. AI assistance: draft, classify, summarize, retrieve facts.
5. Controlled automation: account opening, low-risk message sending.
6. High-risk automation: refund, compensation, address change only after evidence.

## 5. Escalation Rules

Escalate to human review when:

- Platform permission is unavailable.
- API behavior is unknown or undocumented.
- Model confidence is low.
- Facts are missing or conflict.
- Refund, compensation, address change, repeated entitlement, or complaint is involved.
- A test or smoke check fails twice.

## 6. Iteration Output

Each iteration must leave behind:

- Updated docs if scope or architecture changed.
- Code changes with tests.
- QA command output.
- Updated screenshot if the console changed.
- Commit with clear message.

