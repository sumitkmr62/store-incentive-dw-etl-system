from pathlib import Path
import pytest
from incentive_dw.ingestion.file_classifier import classify_file

@pytest.mark.parametrize(
  "file_name, expected_format",
  [
    ("stores.csv", "CSV"),
    ("target.xlsx", "EXCEL"),
    ("employees.json", "JSON"),
    ("events.jsonl", "JSONL"),
    ("directory.xml", "XML"),
    ("sales.parquet", "PARQUET"),
  ],
)
def test_classify_file_identifies_supported_formats(file_name: str, expected_format: str,) -> None:
  result = classify_file(Path(file_name))
  assert result == expected_format 
  
@pytest.mark.parametrize(
  "file_name, expected_format",
  [
    ("STORES.CSV", "CSV"),
    ("TARGETS.XLSX", "EXCEL"),
    ("EMPLOYEES.JSON", "JSON"),
    ("EVENTS.JSONL", "JSONL"),
    ("DIRECTORY.XML", "XML"),
    ("SALES.PARQUET", "PARQUET")
  ],
)
def test_classify_file_handles_uppercase_extensions(file_name, expected_format) -> None:
  result = classify_file(Path(file_name))
  assert result == expected_format
  
def test_classify_file_rejects_unsupported_extensions() -> None:
  file_path = Path("document.txt")
  with pytest.raises(ValueError) as exc_info:
    classify_file(file_path)
    assert "Unsupported file format: .txt" in str(exc_info.value)
    
def test_classify_file_reject_file_without_extensions() -> None:
  file_path = Path("README")
  with pytest.raises(ValueError) as exc_info:
    classify_file(file_path)
    assert "Unsupported file format:" in str(exc_info.value)
  