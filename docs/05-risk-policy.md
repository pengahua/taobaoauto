# Risk and Compliance Policy v0.1

## 1. Hard Boundaries

- Use only official Taobao Open Platform, Qianniu, Cainiao, or allowed service marketplace capabilities.
- Do not use crawler, packet capture, app reverse engineering, simulated login, mass account control, or unofficial automation.
- AppKey, AppSecret, Access Token, and SessionKey must never be shared, logged, or reused across merchants.
- Data use must stay within merchant authorization and real business scenarios.
- If a merchant stops using the app, platform-derived data must be deleted or anonymized according to policy.

## 2. Data Classification

| Level | Data | Requirement |
|---|---|---|
| Public / low-sensitive | Product title, SKU public price, public shop info | Integrity controls |
| Business-sensitive | Order ID, payment state, inventory, cost, shipping strategy | RBAC, audit, backup |
| Personal-sensitive | Receiver name, phone, address, chat record, refund evidence | Encryption, masking, least privilege |
| Secrets | AppSecret, SessionKey, model API key, Cainiao credentials | Secret manager only |

## 3. Privacy Requirements

- Collect minimum fields only.
- Mask personal information by default.
- Decrypt full address or phone only for shipping and after-sales verification.
- Trim and mask model inputs.
- Do not send full order tables, customer databases, cookies, tokens, or secrets into prompts.
- Confirm LLM provider data is not used for training.
- Assess data export or cross-border processing risk if any provider is outside the intended jurisdiction.

## 4. After-sales Automation Boundaries

Can be automatic:

- Logistics query
- Shipping status explanation
- FAQ
- Evidence collection
- Very small compensation within configured limits
- Unshipped cancellation only after warehouse interception check

Human confirmation required:

- Agree refund
- Return refund
- Refund-only request
- Address change
- Reissue or reshipment
- Any money-related compensation
- Suspicious buyer or repeated after-sales case

Manual only:

- Platform intervention
- Complaint or negative review threat
- Legal, invoice, privacy, or account ownership dispute
- High-value item
- High-risk categories
- Signed-for refund-only request
- Any case above configured amount thresholds

## 5. RBAC / ABAC

Roles:

- System administrator
- Operations manager
- Customer service agent
- After-sales specialist
- Finance / owner approver
- Developer / SRE
- Auditor

Rules:

- Role controls broad capabilities.
- Store, amount, risk level, order ownership, and time window control fine-grained access.
- Large refunds, bulk compensation, automation rule changes, and secret rotation require dual approval.
- Full personal information decryption requires reason logging.
- Bot service accounts must be separated from human accounts.

## 6. Required Audit Events

- Login and MFA changes
- Permission changes
- Secret/token access and rotation
- Order sync, waybill, shipment, interception, reissue
- Customer service messages sent by AI
- Refund, compensation, coupon, red packet, price difference
- Automation rule, prompt, and model version changes
- Data export and bulk query
- Personal information decryption
- Risk block and human override

Audit logs must be append-only and must not contain full phone, address, token, cookie, or secret values.

## 7. Launch Gate

Before production:

- API permissions verified in console.
- All data/action paths are official.
- Personal data encryption and masking tested.
- Secrets are absent from code, logs, and plain config.
- Model inputs are trimmed and masked.
- Global kill switches exist for customer message sending, refund, waybill, and shipment.
- Store-level and feature-level kill switches exist.
- Prompt injection tests pass.
- Idempotency tests pass for order sync, account opening, waybill, shipment, and after-sales.
- RBAC/ABAC tests pass.
- Retry tests prove no duplicate refund, duplicate shipment, or duplicate entitlement.
- Production starts as read-only plus suggestion mode, then expands by risk level.

