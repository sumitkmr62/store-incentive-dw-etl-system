"""
Module: csv_header_profiling.py

Purpose:
  Validate the structural quality of CSV column headers

Validations:
  1. CSV file exists and is redable
  2. Header row exists
  3. Columns names are not empty
  4. Column names are not duplicated
"""
import csv
from collections import Counter
from pathlib import Path

#----------------1. Project Configuration----------------------
PROJECT_ROOT = Path(__file__).resolve().parents[4]
SOURCE_DIRECTORY = (
  PROJECT_ROOT
  / "source_system"
  / "store_incentive_synthetic_source_ecosystem"
  / "data"
  / "sqlserver_extracts"
)
# ------------2. Header Validation Function-------------------
def validate_csv_headers(file_path:Path) -> dict:
  """
    Validate the header structure of a single csv file
    file_path (Path) : Path to the csv file
    Returns dict with validation results for the file
  """
  result = {
    "file_name": file_path.name,
    "status": "PASSED",
    "column_count": 0,
    "duplicate_headers": [],
    "empty_headers": [],
    "error": None
  }
  try:
    with file_path.open(
      mode = "r",
      encoding = "utf-8-sig",
      newline = ""
    ) as file:
      reader = csv.reader(file)

      # Read only the first CSV record.
      headers = next(reader, None)

      # Check whether a header exists.
      if not headers:
        result["status"] = "FAILED"
        result["error"] = "Missing or empty header row"
        return result

      # Remove sorrounding whitespace for validation
      normalized_headers = [header.strip() for header in headers]

      # Identify empty column names
      # with for loop
      for index, header in enumerate(normalized_headers):
        if not header:
          result["empty_headers"].append(index + 1)

      # Identify duplicate column names
      header_counts = Counter(normalized_headers)
      result["duplicate_headers"] = [
        header for header, count in header_counts.items() if header and count > 1
      ]
      result["column_count"] = len(headers)

      # Determine the fina; validation status
      if (result["duplicate_headers"] or result['empty_headers']):
        result['status'] = 'FAILED'

  except (OSError, UnicodeDecodeError, csv.Error) as error:
    result['status'] = 'ERROR'
    result["error"] = str(error)
  return result
#----------------3. Source directory profiling--------------------------
"""
Discover CSV Files and validate their headers
source_directory (Path): Directory containing CSV files
Returns: list validation results for all discovered csvs
"""
from pathlib import Path

def profile_csv_directory(source_directory: Path) -> list:

  if not source_directory.exists():
    raise FileNotFoundError(f"Source directory doen not exists: {source_directory}")

  if not source_directory.is_dir():
    raise NotADirectoryError(f"Expected a directory: {source_directory}")

  csv_files = sorted(source_directory.glob("*.csv"))

  if not csv_files:
    raise FileNotFoundError(f"No CSV files found in {source_directory}")

  results = []
  for file_path in csv_files:
    result = validate_csv_headers(file_path)
    results.append(result)
  return results

#---------------4. Display validation results-----------------------
def display_results(results:list) -> None:
  """
  Display individual csv validation results and summary
  """
  passed_count = 0
  failed_count = 0
  error_count = 0

  print("\n" + "=" * 65)
  print("CSV HEADER VALIDATION REPORT")
  print("=" * 65)

  for result in results:
    print(f"\nFile: {result['file_name']}")
    print(f"Status: {result['status']}")
    print(f"Column count: {result['column_count']}")

    if result["duplicate_headers"]:
      print(f"Duplicate headers: {result['duplicate_headers']}")

    if result["empty_headers"]:
      print(f"Empty headers positions: {result['empty_headers']}")

    if result["error"]:
      print(f"Error: {result['error']}")

    if result["status"] == "PASSED":
      passed_count = passed_count + 1

    elif result["status"] == "FAILED":
      failed_count = failed_count + 1

    elif result["status"] == "ERROR":
      error_count = error_count + 1

  print("\n" + "=" * 65)
  print("VALIDATION SUMMARY")
  print("=" * 65)

  print(f"Total CSV files: {len(results)}")
  print(f"Passed: {passed_count}")
  print(f"Failed: {failed_count}")
  print(f"Errors: {error_count}")

  print("=" * 65)

#-------------------5. MAIN EXECUTION----------------------
def main() -> None:
  """
  Main entry point ot the CSV header profiling module
  """
  print("Starting CSV header validation...")

  results = profile_csv_directory(SOURCE_DIRECTORY)
  display_results(results)
  print("\nCSV header validation completed.")

if __name__=='__main__':
  main()