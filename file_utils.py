from pathlib import Path
import file_types

def infer_file_type(file_path: str) -> str:
  extension = Path(file_path).suffix
  return file_types.EXTENSION_TO_TYPE.get(extension.lower(), "unknown")

def get_file_rules(file_type: str) -> dict:
  return file_types.FILE_TYPE_RULES.get(file_type, file_types.FILE_TYPE_RULES["unknown"])

def get_rules_for_extension(extension: str) -> dict:
  file_type = infer_file_type(extension)
  return get_file_rules(file_type)