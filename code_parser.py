import javascript_parser
import os
import python_parser
import go_parser
import ts_parser
import java_parser

def get_functions(file_path):
  # Infer file type by extension
  _, ext = os.path.splitext(file_path)
  ext = ext.lower()
  if ext == ".py":
    # Import here to avoid circular import if any
    return python_parser.get_functions_from_file(file_path)
  elif ext == ".js":
    return javascript_parser.get_functions_from_file(file_path)
  elif ext == ".go":
    return go_parser.get_functions_from_file(file_path)
  elif ext in [".ts", ".tsx"]:
    return ts_parser.get_functions_from_file(file_path)
  elif ext == ".java":
    return java_parser.get_functions_from_file(file_path)
  else:
    print(f"Unsupported file type: {ext}")
    return []
