# Workers

Workers consume domain events and execute persisted commands.

MVP worker groups:

- order sync worker
- customer message worker
- entitlement worker
- waybill worker
- shipment worker
- audit worker

All workers must be idempotent and write audit logs.

