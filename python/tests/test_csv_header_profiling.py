from pathlib import Path
import pytest

from incentive_dw.profiling.csv_header_profiling import (
  validate_csv_headers, profile_csv_directory)

def test_validate_csv_headers_passes_valid_headers(tmp_path:Path)->None:
  csv_file = tmp_path / "stores.csv"
  csv_content = (
    "store_id,store_name,city\n"
    "1,Delhi Vision Store,Delhi\n"
    "2,Gurugram Vision Store,Gurugram\n"
  )
  csv_file.write_text(csv_content,encoding="utf-8")
  result = validate_csv_headers(csv_file)
  assert result["status"] == "PASSED"
  assert result["column_count"] == 3
  
def test_validate_csv_headers_detects_duplicate_headers(tmp_path:Path) -> None:
  csv_file = tmp_path / "store.csv"
  csv_content = (
    "store_id,store_name,city,city\n"
    "1,Delhi Vision Store,Delhi,Delhi\n"
  )
  csv_file.write_text(csv_content, encoding="utf-8")
  result = validate_csv_headers(csv_file)
  assert result["status"] == "FAILED"
  assert result["column_count"] == 4
  assert result["duplicate_headers"] == ['city']
  
def test_validate_csv_headers_detects_empty_headers(tmp_path:Path) -> None:
  csv_file = tmp_path / "store.csv"
  csv_content = (
    "store_id,,city\n"
    "1,Delhi Vision Store,Delhi\n"
  )
  csv_file.write_text(csv_content, encoding="utf-8")
  result = validate_csv_headers(csv_file)
  assert result["column_count"] == 3
  assert result["status"] == "FAILED"
  assert result["empty_headers"] == [2]
  
def test_validate_csv_headers_detects_missing_headers(tmp_path:Path) -> None:
  csv_file = tmp_path / 'store.csv'
  csv_content = ("")
  csv_file.write_text(csv_content, encoding="utf-8")
  result = validate_csv_headers(csv_file)
  assert result["status"] == "FAILED"
  assert result["column_count"] == 0
  assert result["error"] == "Missing or empty header row"
  
def test_validate_csv_headers_handles_missing_file(tmp_path: Path) -> None:
  # 1. Arrange: Build a Path object inside tmp_path without creating the file on disk
  missing_csv_file = tmp_path / "store.csv" 
  
  #2. Act: Pass the non existence file path into validate_csv_header
  result = validate_csv_headers(missing_csv_file)
  
  # 3. Assert: Verify the exception handler caught FileNotFoundError (via OSError)
  assert result["status"] == "ERROR"
  assert result["error"] is not None

def test_validate_csv_headers_handles_invalid_encoding(tmp_path: Path) -> None:
  # 1. Arrange: Create a csv file with invalid UTF-8 bytes
  invalid_utf_file = tmp_path / "store.csv"
  invalid_utf_file.write_bytes(b"\xff")
  
  # 2. Act: Pass the invalid_utf_file into validate_csv_header
  result = validate_csv_headers(invalid_utf_file)
  
  # 3. Assert: 
  assert result["status"] == "ERROR"
  assert result["error"] is not None
  assert "codec can't decode" in result["error"]
  
def test_profile_csv_directory_returns_results_for_all_csv_files(tmp_path:Path) -> None:
  csv_valid_header = tmp_path / "store.csv"
  csv_duplicate_headers = tmp_path / "employees.csv"
  
  csv_content_valid_header = ("store_id,store_name,city\n")
  csv_content_duplicate_headers = ("employee_id,employee_name,status,status\n")
  
  csv_valid_header.write_text(csv_content_valid_header, encoding="utf-8")
  csv_duplicate_headers.write_text(csv_content_duplicate_headers, encoding="utf-8")
  
  result = profile_csv_directory(tmp_path)
  
  assert len(result) == 2
  
  for csv_file_dict in result:
    if csv_file_dict["file_name"] == "employees.csv":
      assert csv_file_dict["file_name"] == "employees.csv"
      assert csv_file_dict["status"] == "FAILED"
      assert csv_file_dict["duplicate_headers"] == ["status"]
    elif csv_file_dict["file_name"] == "store.csv":
      assert csv_file_dict["file_name"] == "store.csv"
      assert csv_file_dict["status"] == "PASSED"
      assert csv_file_dict["duplicate_headers"] == []

def test_profile_csv_directory_raises_error_when_no_csv_files(tmp_path: Path) -> None:
  with pytest.raises(FileNotFoundError) as exc_info:
    profile_csv_directory(tmp_path)
  
  assert "No CSV files found in" in str(exc_info)
    
    
  
    
      
