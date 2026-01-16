import os
import re

def get_functions_from_file(file_path):
    """
    Extracts function names and their code from a JavaScript file.

    Args:
        repo_name (str): Name of the repository (unused, for interface compatibility)
        file_path (str): Path to the JavaScript file

    Returns:
        list: List of tuples (function_name, function_code) found in the file, empty list if none found
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError, IOError):
        return []

    # Patterns for function declarations, function expressions, and arrow functions
    # 1. function foo(...) { ... }
    func_decl_pattern = re.compile(
        r'(function\s+([a-zA-Z0-9_$]+)\s*\([^)]*\)\s*\{)', re.MULTILINE)
    # 2. const foo = function(...) { ... }
    func_expr_pattern = re.compile(
        r'(?:var|let|const)\s+([a-zA-Z0-9_$]+)\s*=\s*function\s*\([^)]*\)\s*\{', re.MULTILINE)
    # 3. const foo = (...) => { ... }
    arrow_func_pattern = re.compile(
        r'(?:var|let|const)\s+([a-zA-Z0-9_$]+)\s*=\s*\([^)]*\)\s*=>\s*\{', re.MULTILINE)
    # 4. const foo = async (...) => { ... }
    arrow_func_async_pattern = re.compile(
        r'(?:var|let|const)\s+([a-zA-Z0-9_$]+)\s*=\s*async\s*\([^)]*\)\s*=>\s*\{', re.MULTILINE)

    # Find all function start positions and names
    matches = []
    for m in func_decl_pattern.finditer(content):
        matches.append((m.start(1), m.group(2)))
    for m in func_expr_pattern.finditer(content):
        matches.append((m.start(0), m.group(1)))
    for m in arrow_func_pattern.finditer(content):
        matches.append((m.start(0), m.group(1)))
    for m in arrow_func_async_pattern.finditer(content):
        matches.append((m.start(0), m.group(1)))

    # Sort by position in file
    matches.sort()

    functions = []
    for idx, (start_pos, func_name) in enumerate(matches):
        # Find the opening brace
        brace_pos = content.find('{', start_pos)
        if brace_pos == -1:
            continue

        # Find the matching closing brace for the function body
        brace_count = 0
        pos = brace_pos
        end_pos = None
        while pos < len(content):
            if content[pos] == '{':
                brace_count += 1
            elif content[pos] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_pos = pos + 1
                    break
            pos += 1
        if end_pos is None:
            continue  # Malformed function, skip

        function_code = content[start_pos:end_pos]
        functions.append((func_name, function_code))

    return functions
