import ast
import os
import sys


def get_functions_from_file(file_path):
  """
  Extracts function names and their code from a code file.
  
  Args:
    file_path (str): Path to the code file to analyze
    
  Returns:
    list: List of tuples (function_name, function_code) found in the file, empty list if none found
  """

  # Check if file exists and is readable
  if not os.path.exists(file_path):
    return []
  
  try:
    with open(file_path, 'r', encoding='utf-8') as file:
      content = file.read()
  except (UnicodeDecodeError, PermissionError, IOError):
    return []
  
  tree = ast.parse(content)
  
  # If it's valid Python, use AST to extract function names and code
  functions = []
  for node in ast.walk(tree):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
      # Get the function name
      function_name = node.name
      
      # Get the function code by extracting the source lines
      start_line = node.lineno - 1  # AST uses 1-based indexing
      end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 1
      
      # Split content into lines and extract the function
      lines = content.split('\n')
      function_lines = lines[start_line:end_line]
      function_code = '\n'.join(function_lines)
      
      functions.append((function_name, function_code))
  
  return functions