import os
import re

def get_functions_from_file(file_path):
    """
    Extracts function/method names and their code from a Java file.

    Args:
        file_path (str): Path to the Java file

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

    # Remove single-line comments to avoid false matches
    content = re.sub(r'//.*', '', content)
    
    # Remove multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # Pattern for Java method declarations
    # Matches: [access_modifier] [static] [final] [synchronized] [native] [abstract] [returnType] methodName(parameters) [throws] { ... }
    # Also handles generics like <T> and constructor methods
    method_pattern = re.compile(
        r'((?:public|private|protected|static|final|synchronized|native|abstract|\s)*)'  # modifiers
        r'(?:<[^>]*>)?'  # optional generics
        r'\s*'
        r'([a-zA-Z_$][a-zA-Z0-9_$<>\[\]]*)'  # return type (or constructor name)
        r'\s+'
        r'([a-zA-Z_$][a-zA-Z0-9_$]*)'  # method name
        r'\s*\('  # opening parenthesis
        r'([^)]*)'  # parameters
        r'\)'  # closing parenthesis
        r'(?:\s*throws\s+[^{]*)?'  # optional throws clause
        r'\s*\{',  # opening brace
        re.MULTILINE | re.DOTALL
    )

    # Special pattern for constructors (no return type)
    constructor_pattern = re.compile(
        r'((?:public|private|protected|\s)*)'  # modifiers
        r'([A-Z][a-zA-Z0-9_$]*)'  # constructor name (class name, starts with capital)
        r'\s*\('  # opening parenthesis
        r'([^)]*)'  # parameters
        r'\)'  # closing parenthesis
        r'(?:\s*throws\s+[^{]*)?'  # optional throws clause
        r'\s*\{',  # opening brace
        re.MULTILINE | re.DOTALL
    )

    # Find all method start positions and names
    matches = []
    
    for match in method_pattern.finditer(content):
        start_pos = match.start()
        return_type = match.group(2).strip()
        method_name = match.group(3).strip()
        
        # Skip if this looks like a constructor (return type same as method name)
        if return_type != method_name:
            matches.append((start_pos, method_name))
    
    # Find constructors
    for match in constructor_pattern.finditer(content):
        start_pos = match.start()
        constructor_name = match.group(2).strip()
        matches.append((start_pos, constructor_name))

    # Sort by position in file
    matches.sort()

    functions = []
    for idx, (start_pos, func_name) in enumerate(matches):
        # Find the opening brace
        brace_pos = content.find('{', start_pos)
        if brace_pos == -1:
            continue

        # Find the matching closing brace for the method body
        brace_count = 0
        pos = brace_pos
        end_pos = None
        in_string = False
        in_char = False
        escape_next = False
        
        while pos < len(content):
            char = content[pos]
            
            # Handle escape sequences
            if escape_next:
                escape_next = False
                pos += 1
                continue
                
            if char == '\\' and (in_string or in_char):
                escape_next = True
                pos += 1
                continue
            
            # Handle string literals
            if char == '"' and not in_char:
                in_string = not in_string
            elif char == "'" and not in_string:
                in_char = not in_char
            elif not in_string and not in_char:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_pos = pos + 1
                        break
            pos += 1
        
        if end_pos is None:
            continue  # Malformed method, skip

        function_code = content[start_pos:end_pos]
        functions.append((func_name, function_code))

    return functions 