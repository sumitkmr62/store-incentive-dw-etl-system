
import csv
from pathlib import Path


def read_csv_records(file_path: Path):
  if not file_path.exists():
    raise FileNotFoundError("File path does not exists")
  elif not file_path.is_file():
    raise IsADirectoryError("Expected a file but received a directory")

  with file_path.open(
    mode="r",
    encoding = "utf-8-sig",
    newline=""
    ) as csv_file:

    csv_reader = csv.DictReader(csv_file)
    if not csv_reader.fieldnames:
      raise ValueError("CSV file is empty or missing a header")

    for row in csv_reader:
      yield row