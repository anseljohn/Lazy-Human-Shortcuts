from lhs.llm import prompt, LLMOpts, LLMType
from lhs.logger import LOG, LogLevel, OUTPUT, DEBUG, INFO, WARNING, ERROR
import re
import string
import shutil

import lhs.system_prompts as system_prompts 

def analyze_query_complexity(query: str) -> tuple[LLMType, int]:
    """
    Analyze query complexity using heuristics to determine the best model to use.
    
    Complexity factors:
    - Query length and word count
    - Technical terms and programming concepts
    - Multi-step operations
    - Conditional logic indicators
    - File system operations
    - Network/system operations
    - Data processing operations
    - Error handling requirements
    - External tool requirements
    - Basic bash vs external tools
    """
    query_lower = query.lower().strip()
    words = query_lower.split()
    word_count = len(words)
    
    # Initialize complexity score
    complexity_score = 0
    
    # 1. Length-based scoring
    if word_count <= 5:
        complexity_score += 1  # Very simple
    elif word_count <= 10:
        complexity_score += 2  # Simple
    elif word_count <= 20:
        complexity_score += 3  # Medium
    elif word_count <= 30:
        complexity_score += 4  # Complex
    else:
        complexity_score += 5  # Very complex
    
    # 2. Technical terms and programming concepts
    technical_terms = [
        'api', 'json', 'xml', 'database', 'sql', 'regex', 'pattern', 'algorithm',
        'function', 'method', 'class', 'object', 'variable', 'loop', 'condition',
        'script', 'automation', 'integration', 'deployment', 'configuration',
        'environment', 'dependency', 'package', 'module', 'library', 'framework',
        'protocol', 'socket', 'thread', 'process', 'memory', 'cache', 'buffer',
        'encryption', 'authentication', 'authorization', 'token', 'session',
        'compilation', 'build', 'test', 'debug', 'log', 'monitor', 'backup',
        'restore', 'migrate', 'sync', 'parse', 'validate', 'transform', 'convert'
    ]
    
    tech_term_count = sum(1 for term in technical_terms if term in query_lower)
    complexity_score += min(tech_term_count * 2, 10)  # Cap at 10 points
    
    # 3. Multi-step operations indicators
    multi_step_indicators = [
        'then', 'after', 'before', 'first', 'second', 'next', 'finally',
        'step', 'stage', 'phase', 'process', 'workflow', 'pipeline',
        'and then', 'followed by', 'subsequently', 'afterward'
    ]
    
    multi_step_count = sum(1 for indicator in multi_step_indicators if indicator in query_lower)
    complexity_score += multi_step_count * 3
    
    # 4. Conditional logic indicators
    conditional_indicators = [
        'if', 'else', 'when', 'unless', 'while', 'until', 'case', 'switch',
        'condition', 'check', 'verify', 'validate', 'test', 'compare',
        'depending on', 'based on', 'according to', 'if exists', 'if not'
    ]
    
    conditional_count = sum(1 for indicator in conditional_indicators if indicator in query_lower)
    complexity_score += conditional_count * 2
    
    # 5. File system operations complexity
    file_ops = {
        'simple': ['list', 'show', 'display', 'find', 'search', 'count'],
        'medium': ['copy', 'move', 'rename', 'create', 'delete', 'backup'],
        'complex': ['sync', 'merge', 'diff', 'patch', 'compress', 'extract', 'mount']
    }
    
    for complexity, ops in file_ops.items():
        op_count = sum(1 for op in ops if op in query_lower)
        if complexity == 'simple':
            complexity_score += op_count
        elif complexity == 'medium':
            complexity_score += op_count * 2
        else:  # complex
            complexity_score += op_count * 3
    
    # 6. Network/system operations
    network_ops = [
        'download', 'upload', 'fetch', 'curl', 'wget', 'http', 'https',
        'api', 'rest', 'websocket', 'ssh', 'scp', 'rsync', 'ftp', 'sftp',
        'ping', 'traceroute', 'nslookup', 'dig', 'telnet', 'netcat'
    ]
    
    network_count = sum(1 for op in network_ops if op in query_lower)
    complexity_score += network_count * 3
    
    # 7. Data processing operations
    data_ops = [
        'parse', 'extract', 'filter', 'sort', 'group', 'aggregate', 'sum',
        'average', 'count', 'transform', 'convert', 'format', 'encode',
        'decode', 'encrypt', 'decrypt', 'hash', 'compress', 'decompress'
    ]
    
    data_count = sum(1 for op in data_ops if op in query_lower)
    complexity_score += data_count * 2
    
    # 8. Error handling and robustness indicators
    error_indicators = [
        'error', 'exception', 'fail', 'retry', 'timeout', 'fallback',
        'backup', 'recovery', 'safe', 'secure', 'validate', 'verify',
        'check', 'ensure', 'guarantee', 'robust', 'reliable'
    ]
    
    error_count = sum(1 for indicator in error_indicators if indicator in query_lower)
    complexity_score += error_count * 2
    
    # 9. Special characters and syntax complexity
    special_chars = sum(1 for char in query if char in '{}[]()<>|&;`$')
    complexity_score += min(special_chars, 5)
    
    # 10. Punctuation complexity (indicates structured thinking)
    punctuation_count = sum(1 for char in query if char in ',.;:!?')
    complexity_score += min(punctuation_count // 2, 3)
    
    # 11. Capitalization patterns (indicates technical terms)
    capital_words = sum(1 for word in words if word[0].isupper() and len(word) > 1)
    complexity_score += min(capital_words, 3)
    
    # 12. Number of sentences (indicates multi-part requests)
    sentences = re.split(r'[.!?]+', query)
    sentence_count = len([s for s in sentences if s.strip()])
    complexity_score += min(sentence_count - 1, 4)
    
    # 13. EXTERNAL TOOL REQUIREMENT ANALYSIS
    external_tool_score = analyze_external_tool_requirements(query_lower)
    complexity_score += external_tool_score
    
    # Determine complexity level based on score
    if complexity_score <= 8:
        return LLMType.SIMPLE, complexity_score
    elif complexity_score <= 15:
        return LLMType.MID, complexity_score
    else:
        return LLMType.COMPLEX, complexity_score

def analyze_external_tool_requirements(query: str) -> int:
    """
    Analyze whether the query requires external tools or can be done with basic bash.
    Returns a complexity score based on tool requirements.
    """
    score = 0
    
    # Basic bash commands (built-in or commonly available)
    basic_bash_commands = {
        'file_ops': ['ls', 'cat', 'echo', 'touch', 'mkdir', 'rm', 'cp', 'mv', 'chmod', 'chown'],
        'text_ops': ['grep', 'sed', 'awk', 'sort', 'uniq', 'wc', 'head', 'tail', 'cut', 'tr'],
        'system_ops': ['ps', 'top', 'kill', 'pkill', 'pgrep', 'df', 'du', 'free', 'uptime'],
        'network_basic': ['ping', 'hostname', 'whoami', 'id', 'groups', 'users'],
        'shell_ops': ['cd', 'pwd', 'export', 'unset', 'alias', 'unalias', 'history']
    }
    
    # External tools that require installation or special setup
    external_tools = {
        'development': ['git', 'docker', 'kubectl', 'helm', 'terraform', 'ansible', 'vagrant'],
        'data_processing': ['jq', 'yq', 'xmlstarlet', 'csvkit', 'pandas', 'numpy', 'sqlite3'],
        'network_advanced': ['curl', 'wget', 'ssh', 'scp', 'rsync', 'nmap', 'netcat', 'telnet'],
        'system_admin': ['systemctl', 'service', 'cron', 'logrotate', 'iptables', 'ufw'],
        'monitoring': ['htop', 'iotop', 'nethogs', 'iftop', 'nagios', 'zabbix'],
        'compression': ['tar', 'gzip', 'bzip2', 'xz', 'zip', 'unzip', '7z'],
        'media': ['ffmpeg', 'imagemagick', 'sox', 'vlc', 'mplayer'],
        'databases': ['mysql', 'postgresql', 'mongodb', 'redis-cli', 'sqlite3'],
        'cloud': ['aws', 'gcloud', 'az', 'doctl', 'vultr-cli'],
        'security': ['openssl', 'gpg', 'ssh-keygen', 'certbot', 'fail2ban']
    }
    
    # Check for basic bash operations (reduce complexity)
    basic_operations = [
        'list', 'show', 'display', 'print', 'echo', 'count', 'find', 'search',
        'read', 'write', 'create', 'delete', 'copy', 'move', 'rename',
        'check', 'verify', 'test', 'compare', 'sort', 'filter'
    ]
    
    basic_count = sum(1 for op in basic_operations if op in query)
    if basic_count > 0:
        score -= min(basic_count, 3)  # Reduce complexity for basic operations
    
    # Check for external tool requirements (increase complexity)
    for category, tools in external_tools.items():
        tool_count = sum(1 for tool in tools if tool in query)
        if tool_count > 0:
            score += tool_count * 3  # Significant complexity increase for external tools
    
    # Check for specific external tool indicators
    external_indicators = [
        'install', 'package', 'dependency', 'library', 'module', 'plugin',
        'api', 'rest', 'graphql', 'websocket', 'database', 'server',
        'container', 'virtual', 'cloud', 'remote', 'ssh', 'ftp',
        'encrypt', 'decrypt', 'hash', 'sign', 'certificate', 'ssl',
        'compress', 'archive', 'backup', 'sync', 'mirror', 'clone',
        'deploy', 'build', 'compile', 'test', 'debug', 'profile',
        'monitor', 'log', 'alert', 'metric', 'dashboard', 'report'
    ]
    
    external_indicator_count = sum(1 for indicator in external_indicators if indicator in query)
    score += external_indicator_count * 2
    
    # Check for programming language requirements
    programming_languages = ['python', 'javascript', 'node', 'npm', 'yarn', 'ruby', 'gem', 'php', 'composer', 'java', 'maven', 'gradle', 'go', 'rust', 'cargo', 'c++', 'gcc', 'make', 'cmake']
    lang_count = sum(1 for lang in programming_languages if lang in query)
    score += lang_count * 4  # High complexity for programming language requirements
    
    # Check for specific file format requirements
    file_formats = ['json', 'xml', 'yaml', 'csv', 'sql', 'html', 'css', 'javascript', 'python', 'bash', 'shell', 'dockerfile', 'kubernetes', 'terraform', 'ansible']
    format_count = sum(1 for fmt in file_formats if fmt in query)
    score += format_count * 2
    
    # Check for system-specific requirements
    system_specific = ['linux', 'ubuntu', 'centos', 'debian', 'macos', 'windows', 'docker', 'kubernetes', 'aws', 'gcp', 'azure']
    system_count = sum(1 for sys in system_specific if sys in query)
    score += system_count * 2
    
    return max(0, score)  # Ensure score doesn't go negative

def orchestrate(query: str):
    # Determine query complexity heuristically
    INFO("Analyzing query complexity...")
    complexity, score = analyze_query_complexity(query)
    DEBUG(f"Query complexity analysis completed: {complexity.value} (score: {score})")
    INFO(f"Complexity: {complexity.value}")
    
    # Use the bash prompt to generate a bash script from the query with appropriate complexity
    INFO("Generating bash script...")
    bash_script = prompt(system_prompts.BASH_PROMPT, query, LLMOpts(complexity=complexity))
    INFO("Bash script generation completed")
    return bash_script