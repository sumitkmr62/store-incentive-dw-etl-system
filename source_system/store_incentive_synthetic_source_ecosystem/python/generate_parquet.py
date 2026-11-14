"""
Convert the supplied JSONL behavioral event extracts to Parquet.
Install dependencies first: pip install -r requirements.txt
Run from the package root: python python/generate_parquet.py
"""
import json
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
JSON_DIR = ROOT / "data" / "json"
PARQUET_DIR = ROOT / "data" / "parquet"
PARQUET_DIR.mkdir(parents=True, exist_ok=True)

def read_jsonl(path):
    rows = []
    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                row = json.loads(line)
                row["event_properties_json"] = json.dumps(row.pop("event_properties", {}), ensure_ascii=False)
                rows.append(row)
    return rows

for source_name, output_name in [
    ("customer_behavior_events.jsonl", "customer_behavior_events.parquet"),
    ("employee_activity_events.jsonl", "employee_activity_events.parquet"),
]:
    records = read_jsonl(JSON_DIR / source_name)
    table = pa.Table.from_pylist(records)
    pq.write_table(table, PARQUET_DIR / output_name, compression="snappy")
    print(f"Created {output_name}: {len(records):,} rows")
