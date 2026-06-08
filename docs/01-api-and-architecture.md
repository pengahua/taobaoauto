# API and Backend Architecture v0.1

## 1. Architecture

```text
External Platforms
  Taobao Open Platform / TOP
  Qianniu customer service APIs
  Cainiao waybill / cloud print APIs
  Internal entitlement / account system
  LLM provider

Access Layer
  OpenAPI Gateway
  OAuth / SessionKey manager
  TOP signing client
  Webhook / RDS / message receiver
  API rate limit and circuit breaker proxy

Domain Services
  Store Service
  Product / SKU Service
  Order Service
  Customer Conversation Service
  Entitlement Service
  Fulfillment Service
  Waybill Service
  Shipment Service
  After-sale Service
  Rule Service

Automation Layer
  LLM Orchestrator
  Tool Gateway
  Intent classifier
  RAG service
  Risk policy engine
  Human handoff decision

Execution Layer
  Command Bus
  Job Workers
  Idempotent executor
  Retry scheduler
  Print adapter
  Notification center

Governance
  PostgreSQL / MySQL
  Redis
  Kafka / RabbitMQ / RocketMQ
  Object storage
  Audit store
  Metrics / tracing / alerting
```

## 2. Integration Matrix

All API availability must be verified in the Taobao Open Platform console before implementation.

| Scenario | Capability / API | Direction | Notes |
|---|---|---|---|
| Authorization | OAuth / SessionKey | Our system -> Taobao | Multi-shop requires per-shop authorization |
| Seller info | `taobao.user.seller.get` | Our system -> TOP | Initialize store profile |
| Initial order sync | `taobao.trades.sold.get` | Our system -> TOP | History and compensation |
| Incremental order sync | `taobao.trades.sold.increment.get` / RDS order push | TOP/RDS -> Our system | Prefer push plus API compensation |
| Order detail | `taobao.trade.fullinfo.get` / simple order detail APIs | Our system -> TOP | Sensitive fields require strict controls |
| Trade memo | `taobao.trade.memo.add/update` | Our system -> TOP | Do not overwrite manual notes blindly |
| Address change | `taobao.trade.shippingaddress.update` | Our system -> TOP | High risk; human confirmation first |
| Shipment | `taobao.logistics.online.send` | Our system -> TOP | Must validate status before shipment |
| Waybill create | `cainiao.waybill.ii.get` | Our system -> Cainiao/TOP | Must be idempotent |
| Waybill query | Cainiao waybill query APIs | Our system -> Cainiao/TOP | Used for compensation and reprint |
| Waybill cancel | `cainiao.waybill.ii.cancel` | Our system -> Cainiao/TOP | Record reason |
| Print templates | `cainiao.cloudprint.stdtemplates.get`, `mystdtemplates.get` | Our system -> Cainiao/TOP | Initialize print settings |
| Qianniu messages | Qianniu message get/send APIs | Our system <-> Qianniu | Use only if permission is available |
| Qianniu tasks | Qianniu task APIs | Our system -> Qianniu | Human handoff |
| Refund list | `taobao.refunds.receive.get` | Our system -> TOP | After-sales entry |
| Refund detail | `taobao.refund.get` | Our system -> TOP | Decision input |
| Refund messages | Refund message APIs | Our system <-> TOP | Evidence and communication |
| Agree refund | Refund agree APIs | Our system -> TOP | High risk; not MVP auto action |
| Refuse refund | Refund refuse APIs | Our system -> TOP | Human-only at first |

## 3. Core Data Model

All tables are multi-tenant and must include `tenant_id` or `store_id`.

```sql
stores(id, tenant_id, platform, seller_id, seller_nick_hash, status, created_at)
store_auth_tokens(id, store_id, app_key, session_key_enc, refresh_token_enc, scopes, expire_at, status)
platform_api_permissions(id, store_id, api_name, granted, quota_limit, last_checked_at)

products(id, store_id, item_id, title, status, raw_json, updated_at)
skus(id, store_id, item_id, sku_id, outer_sku_id, title, price, stock, status)
sku_entitlement_mapping(id, store_id, sku_id, entitlement_product_code, rule_json)

orders(id, store_id, tid, buyer_open_id, status, payment, post_fee, receiver_hash, raw_json, version, modified_at)
order_items(id, order_id, oid, item_id, sku_id, outer_sku_id, num, price, payment, refund_status, raw_json)
order_status_history(id, order_id, from_status, to_status, source, event_id, created_at)
order_address_snapshots(id, order_id, receiver_name_enc, mobile_enc, address_enc, hash, source, created_at)

customer_threads(id, store_id, buyer_open_id, external_thread_id, status, last_message_at)
customer_messages(id, thread_id, direction, sender_type, content_enc, content_hash, attachments_json, external_msg_id, created_at)
customer_intents(id, thread_id, intent, confidence, entities_json, model, created_at)
service_tickets(id, store_id, order_id, thread_id, type, priority, status, assignee, sla_due_at)

entitlement_accounts(id, store_id, buyer_open_id, order_id, status, account_ref, opened_at)
entitlements(id, account_id, order_item_id, product_code, benefit_code, status, start_at, expire_at)
entitlement_commands(id, store_id, order_id, command_type, idempotency_key, status, request_json, result_json)

shipments(id, store_id, order_id, status, carrier_code, logistics_company, waybill_code, package_json)
waybills(id, shipment_id, trade_code, waybill_code, template_id, print_data_json, status, requested_at, printed_at)
print_jobs(id, store_id, waybill_id, printer_id, status, retry_count, last_error, created_at)
delivery_commands(id, store_id, order_id, command_type, idempotency_key, status, external_request_id, result_json)

refunds(id, store_id, refund_id, tid, oid, status, refund_fee, reason, has_good_return, raw_json, modified_at)
refund_actions(id, refund_id, action_type, decision_source, command_id, status, operator, reason, created_at)
refund_messages(id, refund_id, direction, content_enc, attachments_json, external_msg_id, created_at)

platform_events(id, store_id, event_type, external_event_id, aggregate_type, aggregate_id, payload_json, received_at, processed_at)
outbox_events(id, aggregate_type, aggregate_id, event_type, payload_json, status, retry_count, next_retry_at)
commands(id, store_id, command_type, biz_key, idempotency_key, status, payload_json, result_json, locked_until)
api_call_logs(id, store_id, api_name, direction, request_hash, response_code, error_code, latency_ms, trace_id, created_at)

llm_runs(id, store_id, scene, model, prompt_version, input_ref, output_json, risk_level, status, created_at)
automation_decisions(id, store_id, scene, target_type, target_id, decision, confidence, policy_result, human_required)
audit_logs(id, store_id, actor_type, actor_id, action, target_type, target_id, before_json, after_json, trace_id, created_at)
```

## 4. Event Topics

```text
platform.order.changed
platform.refund.changed
platform.message.received
platform.logistics.changed

order.synced
order.paid
order.ready_to_fulfill
order.address_changed
order.cancelled

customer.intent.detected
customer.reply.requested
customer.reply.sent
customer.handoff.required

entitlement.open.requested
entitlement.opened
entitlement.failed

waybill.create.requested
waybill.created
waybill.print.requested
waybill.printed
shipment.consign.requested
shipment.consigned

refund.received
refund.decision.requested
refund.action.requested
refund.action.completed

manual.task.created
audit.event.created
```

## 5. Reliability Requirements

- External write actions must first be persisted as commands.
- Command uniqueness: `unique(store_id, command_type, idempotency_key)`.
- Retry only transient failures: timeout, rate limit, 5xx, platform temporary errors.
- Do not retry business failures: permission denied, invalid state, invalid parameters, waybill service not subscribed.
- Use DLQs by domain: `dlq.order`, `dlq.refund`, `dlq.waybill`, `dlq.customer`.
- Query external state before retrying when local timeout happens after an external write.
- Every event carries `event_id`, `trace_id`, `store_id`, `aggregate_id`, `occurred_at`.
- Partition by `store_id + tid/refund_id/thread_id` to preserve per-object ordering.

