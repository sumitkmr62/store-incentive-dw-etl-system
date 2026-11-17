from pathlib import Path

def classify_file(file_path: Path) -> str:
  file_extension = file_path.suffix.lower()
  extension_mapping = {
    ".csv": "CSV",
    ".xlsx": "EXCEL",
    ".json": "JSON",
    ".jsonl": "JSONL",
    ".xml": "XML",
    ".parquet": "PARQUET",
  }
  if file_extension not in extension_mapping:
    raise ValueError(f"Unsupported file format: {file_extension}")
  return extension_mapping[file_extension]
  