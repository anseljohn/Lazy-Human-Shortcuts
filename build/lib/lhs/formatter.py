import re

def format_bash_output(prompt: str, script: str, output: str) -> str:
    """
    Format bash script output by cleaning up whitespace and formatting.
    
    Args:
        prompt: The original user prompt/request (unused in heuristic approach)
        script: The generated bash script (unused in heuristic approach)
        output: The output from executing the bash script
        
    Returns:
        Cleaned output string ready for display
    """
    if not output or not output.strip():
        return ""
    
    # Remove leading and trailing whitespace
    cleaned = output.strip()
    
    # Split into lines and process each line
    lines = cleaned.split('\n')
    processed_lines = []
    
    for line in lines:
        # Remove leading/trailing whitespace from each line
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Remove excessive whitespace (multiple spaces/tabs become single space)
        line = re.sub(r'\s+', ' ', line)
        
        # Remove common bash prompt artifacts
        # Remove lines that look like shell prompts (e.g., $, #, >, etc.)
        if re.match(r'^[\$#>\]]\s*$', line):
            continue
            
        # Remove lines that are just command echoes
        if line.startswith('$ ') or line.startswith('# '):
            continue
            
        # Remove common bash output artifacts
        # Skip lines that are just separators or decorative
        if re.match(r'^[-=_*]{3,}$', line):
            continue
            
        # Skip lines that are just whitespace or special characters
        if re.match(r'^[\s\-=_*]+$', line):
            continue
            
        processed_lines.append(line)
    
    # Join lines with single newlines
    result = '\n'.join(processed_lines)
    
    # Ensure there's exactly one newline at the end
    result = result.rstrip()
    
    return result
