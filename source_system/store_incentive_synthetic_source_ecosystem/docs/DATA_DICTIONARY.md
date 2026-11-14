# Data Dictionary and Source Notes

## Relational OLTP tables and grain

| Table | Grain | Primary key | Main relationships |
|---|---|---|---|
| retail.Store | One row per store | store_id | Parent of employees, orders, eye tests |
| hr.Employee | One row per employee | employee_id | Store; self-referencing manager |
| retail.Customer | One row per customer | customer_id | Parent of orders and eye tests |
| retail.Product | One row per product/SKU | product_id | Parent of order items |
| retail.SalesOrder | One row per sales order | order_id | Store, customer, sales employee |
| retail.SalesOrderItem | One row per product line in an order | order_line_id | Sales order and product |
| retail.Payment | One payment record per order in this sample | payment_id | Sales order |
| retail.ReturnTxn | One return event per returned order line | return_id | Sales order item |
| hr.Attendance | One employee-day attendance record | attendance_id | Employee |
| clinical.EyeTest | One eye-test record | eye_test_id | Customer, store, optometrist |
| ops.EmployeeMonthlyTarget | One employee-month-target version | target_id | Employee |
| ops.QualityAudit | One employee/store audit event | audit_id | Employee and store |

## File sources

- `customer_behavior_events.jsonl`: one customer event per line; `event_properties` is nested JSON.
- `employee_activity_events.jsonl`: one employee operational event per line; `event_properties` is nested JSON.
- `monthly_targets_and_policy.xlsx`: three worksheets: EmployeeTargets, StoreTargets, PolicyParameters.
- `customer_behavior_events.parquet`: generated locally by `python/generate_parquet.py`; one customer behavioral event per row, with nested event properties retained as a JSON string column.
- `employee_activity_events.parquet`: generated locally by `python/generate_parquet.py`; one employee activity event per row.
- `employee_directory.xml`: hierarchical XML document with one Employee element per employee.
- `store_master.xml`: hierarchical XML document with one Store element per store.

## Synthetic data caveats and intentional quality scenarios

- Data is fictional. Names are generated placeholders.
- Employee manager references are simple illustrative reporting relationships, not a validated real-world hierarchy.
- Some orders are cancelled; corresponding payment status is FAILED and payment amount is zero.
- Returns include APPROVED, RECEIVED and REJECTED statuses.
- Eye tests include COMPLETED, CANCELLED and VOIDED statuses.
- Attendance includes PRESENT, ABSENT, PAID_LEAVE, UNPAID_LEAVE and HALF_DAY.
- Quality scores span below and above illustrative thresholds.
- Behavioral events are independently generated. They are not guaranteed to correspond one-to-one with a particular order, eye test or customer journey. Treat event-to-transaction matching as a data engineering exercise, not as a guaranteed foreign-key relationship.
- Policy parameter values in Excel are illustrative simulation parameters, not approved company policy.

## Recommended initial profiling

1. Compare CSV row counts with SQL table counts after loading.
2. Validate primary-key uniqueness and foreign-key orphans.
3. Check nullability, domain values and date ranges.
4. Reconcile order-line totals to order/payment totals, noting cancellation treatment.
5. Profile attendance and eye-test status distributions.
6. Parse JSON, XML, Excel and Parquet independently before unifying them in Bronze.
