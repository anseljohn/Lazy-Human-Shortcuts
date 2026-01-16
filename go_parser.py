import os
import re

def get_functions_from_file(file_path):
    """
    Extracts function names and their code from a Go file.

    Args:
        file_path (str): Path to the Go file

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

    # Patterns for Go function declarations
    # 1. func funcName(...) { ... }
    # 2. func (receiver Type) funcName(...) { ... } (methods)
    # 3. func funcName(...) returnType { ... }
    # 4. func (receiver Type) funcName(...) returnType { ... } (methods with return type)
    
    # Pattern to match function declarations
    func_pattern = re.compile(
        r'(func\s+(?:\([^)]*\)\s+)?([a-zA-Z0-9_]+)\s*\([^)]*\)(?:\s*[^{]*?)?\s*\{)',
        re.MULTILINE | re.DOTALL
    )

    # Find all function start positions and names
    matches = []
    for match in func_pattern.finditer(content):
        start_pos = match.start()
        func_name = match.group(2)
        matches.append((start_pos, func_name))

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