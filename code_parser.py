import ast
import os
import sys
import re


def get_functions_from_file(repo_name, file_path):
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
  
  # Try to parse the file as Python code
  try:
    tree = ast.parse(content)
  except SyntaxError:
    # Pattern to match function definitions in various languages with their code
    patterns = [
      # Python: def function_name
      (r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\):(.*?)(?=\n\S|\Z)', re.DOTALL),
      # JavaScript/TypeScript: function functionName or const functionName =
      (r'(?:function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{.*?\})|(?:const\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:\([^)]*\)\s*=>\s*\{.*?\}|function\s*\([^)]*\)\s*\{.*?\}))', re.DOTALL),
      # Java/C#: public/private/protected static/final function_name
      (r'(?:public|private|protected|static|final)\s+(?:static\s+)?(?:final\s+)?(?:[a-zA-Z_][a-zA-Z0-9_]*\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{.*?\}', re.DOTALL),
      # C/C++: function_name(
      (r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{.*?\}', re.DOTALL),
      # PHP: function function_name
      (r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{.*?\}', re.DOTALL),
      # Ruby: def function_name
      (r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*.*?(?=\n\s*end|\n\S|\Z)', re.DOTALL),
      # Go: func function_name
      (r'func\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{.*?\}', re.DOTALL),
      # Rust: fn function_name
      (r'fn\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{.*?\}', re.DOTALL),
      # Swift: func function_name
      (r'func\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{.*?\}', re.DOTALL),
      # Kotlin: fun function_name
      (r'fun\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{.*?\}', re.DOTALL),
    ]
    
    functions = []
    for pattern, flags in patterns:
      matches = re.findall(pattern, content, flags)
      for match in matches:
        if isinstance(match, tuple):
          # Handle patterns that return tuples (like JS patterns)
          for name in match:
            if name:
              # Find the actual function code for this name
              name_pattern = rf'(?:function\s+{re.escape(name)}\s*\([^)]*\)\s*{{.*?}})|(?:const\s+{re.escape(name)}\s*=\s*(?:\([^)]*\)\s*=>\s*{{.*?}}|function\s*\([^)]*\)\s*{{.*?}}))'
              code_match = re.search(name_pattern, content, re.DOTALL)
              if code_match:
                functions.append((name, code_match.group(0)))
        else:
          # For single match patterns, extract the function name and code
          if match:
            # Find the complete function code starting from the match
            start_pos = content.find(match)
            if start_pos != -1:
              # For Python, find the function body
              if 'def ' in match:
                # Find the colon and get everything after it
                colon_pos = match.find(':')
                if colon_pos != -1:
                  function_name = re.search(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', match).group(1)
                  # Get the function body with proper indentation
                  body_start = start_pos + colon_pos + 1
                  body = content[body_start:].lstrip()
                  # Find the end of the function (next function or end of file)
                  next_def = re.search(r'\n\s*def\s+', body)
                  if next_def:
                    body = body[:next_def.start()]
                  functions.append((function_name, f"def {function_name}({match[colon_pos+1:].strip()}:{body}"))
              else:
                # For other languages, use the full match
                function_name = re.search(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', match).group(1)
                functions.append((function_name, match))

    return list(set(functions))  # Remove duplicates
  
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
      
      uid = f"{repo_name}/{os.path.relpath(file_path, sys.argv[1])}::{function_name}"
      type = "function"
      name = function_name
      content = function_code


      functions.append((function_name, function_code))
  
  return functions