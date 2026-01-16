import os
import re

def get_functions_from_file(file_path):
    """
    Extracts function names and their code from a TypeScript/TSX file.

    Args:
        file_path (str): Path to the TypeScript/TSX file

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

    # Patterns for TypeScript/TSX function declarations
    # 1. function foo(...): Type { ... }
    func_decl_pattern = re.compile(
        r'(function\s+([a-zA-Z0-9_$]+)\s*\([^)]*\)(?:\s*:\s*[^{]*?)?\s*\{)', re.MULTILINE)
    
    # 2. const foo = function(...): Type { ... }
    func_expr_pattern = re.compile(
        r'(?:var|let|const)\s+([a-zA-Z0-9_$]+)\s*=\s*function\s*\([^)]*\)(?:\s*:\s*[^{]*?)?\s*\{', re.MULTILINE)
    
    # 3. const foo = (...): Type => { ... }
    arrow_func_pattern = re.compile(
        r'(?:var|let|const)\s+([a-zA-Z0-9_$]+)\s*=\s*\([^)]*\)(?:\s*:\s*[^{=]*?)?\s*=>\s*\{', re.MULTILINE)
    
    # 4. const foo = async (...): Type => { ... }
    arrow_func_async_pattern = re.compile(
        r'(?:var|let|const)\s+([a-zA-Z0-9_$]+)\s*=\s*async\s*\([^)]*\)(?:\s*:\s*[^{=]*?)?\s*=>\s*\{', re.MULTILINE)
    
    # 5. async function foo(...): Type { ... }
    async_func_pattern = re.compile(
        r'(async\s+function\s+([a-zA-Z0-9_$]+)\s*\([^)]*\)(?:\s*:\s*[^{]*?)?\s*\{)', re.MULTILINE)
    
    # 6. Method definitions in classes/interfaces/objects
    method_pattern = re.compile(
        r'([a-zA-Z0-9_$]+)\s*\([^)]*\)(?:\s*:\s*[^{]*?)?\s*\{', re.MULTILINE)
    
    # 7. Generic function patterns
    generic_func_pattern = re.compile(
        r'(function\s+([a-zA-Z0-9_$]+)\s*<[^>]*>\s*\([^)]*\)(?:\s*:\s*[^{]*?)?\s*\{)', re.MULTILINE)

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
    
    for m in async_func_pattern.finditer(content):
        matches.append((m.start(1), m.group(2)))
    
    for m in generic_func_pattern.finditer(content):
        matches.append((m.start(1), m.group(2)))
    
    # Find methods (be more selective to avoid false positives)
    for m in method_pattern.finditer(content):
        method_start = m.start()
        method_name = m.group(1)
        
        # Check if this looks like a method definition (preceded by whitespace or certain keywords)
        prefix = content[max(0, method_start - 50):method_start]
        if (any(keyword in prefix for keyword in ['class', 'interface', 'export', 'public', 'private', 'protected', 'static']) or
            re.search(r'^\s*$', prefix) or  # starts at beginning of line
            re.search(r'[,;]\s*$', prefix)):  # follows another method/property
            matches.append((method_start, method_name))

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
        in_string = False
        string_char = None
        
        while pos < len(content):
            char = content[pos]
            
            # Handle string literals to avoid counting braces inside strings
            if char in ['"', "'", '`'] and not in_string:
                in_string = True
                string_char = char
            elif char == string_char and in_string:
                # Check if it's escaped
                if pos > 0 and content[pos-1] != '\\':
                    in_string = False
                    string_char = None
            elif not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
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