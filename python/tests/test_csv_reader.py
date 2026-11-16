from pathlib import Path
from incentive_dw.ingestion.csv_reader import read_csv_records

def test_read_csv_records_return_all_records(tmp_path: Path) -> None:
  # 1. Define a file path inside pytest's isolated temporary directory
  csv_file = tmp_path / "stores.csv"

  # 2. Write the header and three records to the disk
  csv_content = (
    "store_id,store_code,store_name,city,state,region,opening_date,store_status\n"
    "1,STR-001,Delhi Vision Store 01,Delhi,Delhi,North-1,07-02-2020,ACTIVE\n"
    "2,STR-002,Gurugram Vision Store 02,Gurugram,Haryana,North-1,15-03-2020,ACTIVE\n"
    "3,STR-003,Noida Vision Store 03,Noida,Uttar Pradesh,North-1,21-04-2020,ACTIVE\n"
  )
  csv_file.write_text(csv_content, encoding="utf-8-sig")

  # 3 & 4. Invoke the generator and count yielded records without materialiing a list
  record_count = sum(1 for _ in read_csv_records(csv_file))

  # 5. Verify the exact count
  assert record_count == 3
