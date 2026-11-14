# Synthetic Lenskart Store Incentive Source Ecosystem

**Version 1 architecture:** SQL Server 2022 + Python + Medallion Architecture + Power BI.

All records are fictional and generated for engineering practice. They do not represent real customers, employees, transactions, policies or Lenskart operational data.

## Dataset profile

| Entity | Records |
|---|---:|
| Stores | 20 |
| Employees | 200 |
| Customers | 1,000 |
| Products | 200 |
| Sales orders | 15,000 |
| Sales order lines | 50,000 |
| Payments | 15,000 |
| Returns | 1,673 |
| Attendance rows | 28,800 |
| Eye tests | 9,000 |
| Employee monthly targets | 2,000 |
| Quality audits | 400 |
| Customer behavior events | 50,000 |
| Employee activity events | 10,000 |

## Source formats

- SQL Server: normalized OLTP DDL in `sql/01_create_oltp_database.sql`.
- CSV: relational entity extracts in `data/sqlserver_extracts/`.
- JSON / JSONL: nested customer and employee behavioral event payloads in `data/json/`.
- Excel: monthly employee targets, store targets and illustrative policy parameters in `data/excel/`.
- Parquet: reproducible columnar customer and employee event datasets; generate them from the JSONL files using `python/generate_parquet.py` after installing `requirements.txt`. The build environment used for this archive did not have a Parquet engine installed, so the binary Parquet files are not embedded in this ZIP.
- XML: employee directory and store master in `data/xml/`.

## Important implementation boundary

The SQL script creates the OLTP database and relational tables. The CSV files are corresponding source extracts; they are not automatically inserted into SQL Server by running the DDL. Loading them into SQL Server is a separate Python/SQLAlchemy Core implementation task.

The current package is source-system input for the Version 1 Bronze ingestion work. It does not create or populate the `StoreIncentiveDW` warehouse.
