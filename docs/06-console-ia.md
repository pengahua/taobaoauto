# Operations Console Information Architecture v0.1

## 1. Navigation

| Page | Priority | Purpose |
|---|---|---|
| Dashboard | P0 | Overview of automation status, risk holds, task failures |
| Shop Authorization | P0 | Bind shop, check permissions, token status |
| Order Workbench | P0 | View orders, status, risk, fulfillment readiness |
| Customer Service | P1 | Draft replies, inspect facts, hand off to human |
| Waybill & Shipment | P1 | View waybill commands, print jobs, shipment state |
| Entitlement Opening | P1 | SKU mapping, account creation, entitlement grant state |
| Exception Queue | P0 | All blocked tasks requiring attention |
| Policy Rules | P0 | Action thresholds, risk levels, kill switches |
| AI Audit | P0 | LLM runs, prompt version, output, final decision |
| API Audit | P0 | Platform API calls, errors, latency, trace id |
| Settings | P2 | Users, roles, environment, integration settings |

## 2. Dashboard Metrics

- Orders synchronized today
- Pending-shipment orders
- Automation allowed / held / manual required
- Exception queue size
- Waybill creation success
- Shipment command success
- AI draft count
- Policy holds
- API failure rate

## 3. Order Workbench Fields

- Store
- TID
- Buyer masked ID
- Payment
- Order status
- Refund status
- SKU mapping status
- Fulfillment type
- Risk level
- Automation decision
- Latest exception
- Updated time

## 4. Exception Queue Types

- Missing permission
- API failure
- Missing SKU mapping
- Refund in progress
- Low AI confidence
- Policy hold
- Missing verified facts
- Duplicate command blocked
- Manual approval required

## 5. Policy Rules MVP

- Global kill switch
- Shop-level kill switch
- Customer message auto-send enabled
- Waybill auto-create enabled
- Shipment auto-mark enabled
- Refund actions enabled
- Maximum automatic compensation amount
- High-risk keywords
- Force-human categories

