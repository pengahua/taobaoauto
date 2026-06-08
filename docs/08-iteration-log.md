# Iteration Log

## 2026-06-08 - Sprint 0 / Engineering Baseline

### Completed

- Created project charter, MVP PRD, API matrix, AI agent spec, risk policy, console IA, and 12-week plan.
- Built FastAPI backend skeleton.
- Built React operations console.
- Added policy engine, command bus, idempotent executor, audit service, risk levels, kill switches, and tool registry.
- Added dashboard API for frontend integration.
- Added SQLAlchemy base models for stores, orders, commands, and audit logs.
- Added order state machine and shipment safety checks.
- Connected frontend to dashboard and policy APIs.
- Added backend unit tests and QA smoke script.

### Validation

- Backend unit tests.
- Frontend TypeScript build.
- Backend health endpoint.
- Dashboard summary endpoint.
- Playwright frontend render smoke.

### Next Iteration

- Add real persistence repositories.
- Add Taobao OAuth callback flow.
- Add TOP signing adapter contract tests.
- Add order sync command handler.
- Add exception queue storage and UI data binding.
- Add prompt/RAG redaction pipeline.

## 2026-06-08 - Sprint 0 / Autonomous Loop

### Completed

- Added autonomous operating model for product, backend, AI, risk, frontend, QA, and SRE roles.
- Added iteration loop script that starts local services and runs QA smoke checks.
- Added prioritized backlog for the next implementation wave.

### Principle

No iteration is complete until the loop passes: tests, build, API health, dashboard API, browser smoke, and git status review.

## 2026-06-08 - Sprint 1 / Integration Foundations

### Completed

- Added repository layer for orders, commands, and audit logs.
- Added Taobao OAuth URL builder and callback acceptance endpoint.
- Added TOP request signing helper and contract tests.
- Added order sync command handler with idempotency, status history, and audit write.
- Added exception task API with owner roles and next actions.
- Connected frontend console to exception queue API.

### Validation

- Backend tests increased to 16 and pass.
- Frontend build passes.
- Iteration loop passes.
- Browser smoke confirms exception queue renders with Risk Lead and Taobao Integration ownership.

### Next

- Add Alembic migrations or a lightweight migration strategy.
- Add persistent API call log wrapper for TOP adapters.
- Add real order pull adapter boundary and fixture-based contract tests.
- Add exception queue persistence instead of static seed data.

## 2026-06-08 - Sprint 1 / Safety Persistence

### Completed

- Added persistent models for API call logs, exception tasks, and kill switches.
- Added repositories for API logs, exception tasks, and kill switches.
- Added Taobao TOP client and order adapter request preparation.
- Added platform API proxy recording for signed TOP requests.
- Added risk kill-switch API and frontend binding.
- Moved exception queue from static response to database-backed seed/read flow.
- Cleaned the frontend console source into a readable UTF-8 implementation.

### Validation

- Backend adapter and API log tests added.
- Risk kill-switch API tests added.
- QA smoke script now checks risk kill-switch API.

### Next

- Add a migration tool and versioned schema changes.
- Implement real TOP HTTP execution behind the proxy with timeout and retry policy.
- Add persisted order workbench API and UI table.
- Add shop token storage with encrypted fields.

## 2026-06-09 - Sprint 2 / DeepSeek Auto Reply

### Completed

- Added configurable DeepSeek provider settings.
- Added DeepSeek chat completion client using OpenAI-compatible `/chat/completions`.
- Added LLM redaction for phone numbers, long order IDs, and sensitive fact keys.
- Added customer auto-reply orchestration with intent classification, risk classification, fallback reply, and auto-send gate.
- Added `/api/ai/customer-auto-reply` endpoint.
- Added frontend DeepSeek auto-reply lab for buyer-message testing.

### Safety

- Auto-send remains disabled by default.
- High-risk keywords such as refund, complaint, address change, compensation, and platform intervention force human review.
- DeepSeek receives redacted buyer messages and redacted facts only.
- Without `DEEPSEEK_API_KEY`, the system uses deterministic safe fallback replies.

### Validation

- Added tests for redaction, intent/risk classification, fallback reply, and API endpoint.
- Added Qianniu message send request preparation contract.
- Added AI auto-reply endpoint to QA smoke gate.
