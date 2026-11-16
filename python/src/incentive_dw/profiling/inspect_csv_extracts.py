import csv
from pathlib import Path

# 1. Define the directory containing csv files
project_root = Path(__file__).resolve().parents[4]

# 2. Locate the directory containing CSV files
source_dir = (
  project_root /
  "source_system" /
  "store_incentive_synthetic_source_ecosystem" /
  "data" /
  "sqlserver_extracts"
  )

# 2. Find every CSV files in the directory
for file_path in sorted(source_dir.glob("*.csv")):
  # 3. Open the current CSV file
  with file_path.open(
    "r",
    encoding="utf-8-sig",
    newline = ""
  ) as file:

  # 4. Read the CSV using its first row as column header
    reader = csv.DictReader(file)

    # 5. Count the data records
    row_count = sum(1 for _ in reader)

    #6. Display the results
    print(f"\nFile: {file_path.name}")
    print(f"Columns: {reader.fieldnames}")
    print(f"Records: {row_count}")