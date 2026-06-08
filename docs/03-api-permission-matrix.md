# API Permission Matrix v0.1

This matrix is a planning artifact. Every API must be verified in Taobao Open Platform before implementation.

| Capability | Candidate API / Channel | MVP | Risk | Notes |
|---|---|---:|---|---|
| OAuth authorization | Taobao OAuth / SessionKey | Yes | Medium | Per-shop authorization |
| Seller profile | `taobao.user.seller.get` | Yes | Low | Store initialization |
| Historical orders | `taobao.trades.sold.get` | Yes | Medium | Use for bootstrap and reconciliation |
| Incremental orders | RDS order push / `taobao.trades.sold.increment.get` | Yes | Medium | Push plus compensation preferred |
| Order detail | `taobao.trade.fullinfo.get` or simple detail APIs | Yes | High | Contains sensitive fields |
| Trade memo | `taobao.trade.memo.add/update` | Later | Medium | Avoid overwriting manual notes |
| Shipping address update | `taobao.trade.shippingaddress.update` | No | High | Human-only initially |
| Waybill creation | `cainiao.waybill.ii.get` | Yes | Medium | Idempotent command |
| Waybill query | Cainiao waybill query APIs | Yes | Low | Compensation and reprint |
| Waybill cancel | `cainiao.waybill.ii.cancel` | Later | Medium | Requires reason and audit |
| Print templates | Cainiao cloud print template APIs | Yes | Low | Setup and print preview |
| Shipment callback | `taobao.logistics.online.send` | Yes | High | Validate paid, not refunding, not shipped |
| Qianniu message read | Qianniu message APIs | Yes if available | High | Permission may vary |
| Qianniu message send | Qianniu message send APIs | Later | High | Draft mode first |
| Qianniu task | Qianniu task APIs | Later | Medium | Human handoff |
| Refund list | `taobao.refunds.receive.get` | Later | High | Assist only |
| Refund detail | `taobao.refund.get` | Later | High | Assist only |
| Refund agree/refuse | Refund action APIs | No | Critical | Human-only until V2 evidence |

## MVP Permission Verification Tasks

1. Create developer app.
2. Confirm OAuth redirect and app category.
3. Request order read permissions.
4. Request product/SKU read permissions.
5. Request Cainiao waybill permissions.
6. Confirm Qianniu message availability for target merchant scenario.
7. Document unavailable APIs and degraded alternatives.

