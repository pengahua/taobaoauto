# Taobao Autopilot Commerce

Production-oriented Taobao/Tmall commerce automation platform.

The project is designed around official Taobao Open Platform, Qianniu, Cainiao waybill APIs, and LLM agents. LLMs assist with understanding, generation, triage, and orchestration; state machines, rule engines, audit, and human approvals own final execution.

## Workspace

```text
backend/   FastAPI service, domain modules, integrations, workers
frontend/  React operations console
docs/      Project charter, architecture, risk policy, execution plan
```

## First Milestone

MVP focuses on:

- Shop authorization foundation
- Order synchronization model
- Customer service AI suggestion mode
- Waybill and shipment task visibility
- Exception queue
- Audit and policy controls

High-risk after-sales automation is intentionally excluded from MVP.

## Local Development

Backend:

```powershell
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Optional DeepSeek environment:

```powershell
$env:DEEPSEEK_API_KEY="your_key"
$env:DEEPSEEK_MODEL="deepseek-chat"
$env:AI_AUTO_SEND_ENABLED="false"
```

Frontend:

```powershell
cd frontend
npm install
npm run dev -- --port 5173
```

Smoke validation:

```powershell
.\scripts\qa-smoke.ps1
```

Autonomous iteration loop:

```powershell
.\scripts\iteration-loop.ps1
```
