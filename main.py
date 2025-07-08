import os
import sys
from re import A
from CKGNode import CKGNode
from build_ckg import build_ckg

def is_text_file(file_path):
  """
  Determines if a file can be opened by a text editing program.
  
  Args:
    file_path (str): Path to the file to check
    
  Returns:
    bool: True if the file is a text file, False otherwise
  """
  # Comprehensive list of text file extensions
  text_extensions = {
    # Programming languages
    '.py', '.pyw', '.pyx', '.pyi', '.pxd', '.pyx', '.pyo', '.pyd',
    '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs',
    '.java', '.class', '.jar', '.war', '.ear',
    '.cpp', '.cc', '.cxx', '.c++', '.c', '.h', '.hpp', '.hxx', '.hh',
    '.cs', '.vb', '.vbs', '.asp', '.aspx', '.ashx', '.asmx',
    '.php', '.phtml', '.php3', '.php4', '.php5', '.phps',
    '.rb', '.erb', '.rake', '.gemspec', '.podspec',
    '.go', '.mod', '.sum',
    '.rs', '.toml',
    '.swift', '.playground',
    '.kt', '.kts',
    '.scala', '.sbt',
    '.dart',
    '.r', '.R',
    '.m', '.mm', '.M',
    '.pl', '.pm', '.t', '.pod',
    '.lua', '.lua',
    '.sh', '.bash', '.zsh', '.fish', '.ksh', '.csh', '.tcsh',
    '.bat', '.cmd', '.ps1', '.psm1', '.psd1',
    '.sql', '.ddl', '.dml', '.pgsql', '.mysql',
    '.html', '.htm', '.xhtml', '.shtml', '.jhtml',
    '.xml', '.xsl', '.xslt', '.xsd', '.dtd', '.rss', '.atom',
    '.css', '.scss', '.sass', '.less', '.styl',
    '.json', '.jsonc', '.json5', '.jsonl',
    '.yaml', '.yml',
    '.toml',
    '.ini', '.cfg', '.conf', '.config', '.cnf',
    '.properties', '.props',
    '.env', '.env.local', '.env.development', '.env.production',
    '.gitignore', '.gitattributes', '.gitmodules',
    '.dockerfile', '.dockerignore',
    '.makefile', '.mk', '.mak',
    '.cmake', '.cmake.in',
    '.gradle', '.gradle.kts',
    '.pom.xml', '.build.xml', '.ant.xml',
    '.package.json', '.package-lock.json', '.yarn.lock',
    '.requirements.txt', '.setup.py', '.pyproject.toml',
    '.composer.json', '.composer.lock',
    '.gemfile', '.gemfile.lock',
    '.cargo.toml', '.cargo.lock',
    '.go.mod', '.go.sum',
    '.pubspec.yaml', '.pubspec.lock',
    '.podfile', '.podfile.lock',
    '.cartfile', '.cartfile.resolved',
    '.swift.package', '.swift.package.resolved',
    '.csproj', '.vbproj', '.sln', '.vcxproj', '.vcxproj.filters',
    '.pro', '.pri', '.qrc', '.ui', '.qml',
    '.asm', '.s', '.S', '.inc', '.nasm', '.masm',
    '.f', '.f90', '.f95', '.f03', '.f08',
    '.pas', '.pp', '.p', '.inc',
    '.ada', '.adb', '.ads',
    '.cob', '.cbl', '.cpy',
    '.d', '.di',
    '.nim',
    '.zig',
    '.v', '.sv',
    '.hs', '.lhs',
    '.ml', '.mli', '.mll', '.mly',
    '.clj', '.cljs', '.cljc', '.edn',
    '.el', '.elc',
    '.scm', '.ss', '.rkt',
    '.tcl', '.tk',
    '.awk', '.gawk',
    '.sed',
    '.tex', '.ltx', '.sty', '.cls', '.bbl', '.aux',
    '.rst', '.rest',
    '.md', '.markdown', '.mdown', '.mkdn',
    '.txt', '.text', '.asc', '.nfo',
    '.csv', '.tsv', '.tab',
    '.log', '.out', '.err',
    '.lock', '.lockfile',
    '.map', '.sourcemap',
    '.d.ts', '.d.ts.map',
    '.min.js', '.min.css',
    '.template', '.tmpl', '.tpl',
    '.ejs', '.jade', '.pug', '.haml', '.slim',
    '.vue', '.svelte', '.jsx', '.tsx',
    '.graphql', '.gql',
    '.proto', '.protobuf',
    '.thrift',
    '.avdl', '.avpr', '.avsc',
    '.wsdl', '.xsd',
    '.wsgi', '.asgi',
    '.nginx', '.apache', '.htaccess',
    '.systemd', '.service', '.socket', '.timer',
    '.cron', '.crontab',
    '.hosts', '.fstab', '.passwd', '.group',
    '.ssh', '.ssh_config', '.ssh_known_hosts',
    '.vim', '.vimrc', '.gvimrc',
    '.emacs', '.elisp',
    '.sublime-project', '.sublime-workspace',
    '.vscode', '.code-workspace',
    '.idea', '.iml',
    '.xcconfig', '.plist',
    '.reg', '.inf', '.ini',
    '.conf', '.cnf', '.cfg',
    '.yaml', '.yml', '.yaml.schema',
    '.json.schema', '.jsonld',
    '.rdf', '.owl', '.ttl', '.n3',
    '.sparql', '.rq',
    '.cypher', '.cql',
    '.sqlite', '.db', '.sql',
    '.mdb', '.accdb',
    '.xlsx', '.xls', '.csv',
    '.docx', '.doc', '.rtf',
    '.pptx', '.ppt',
    '.odt', '.ods', '.odp',
    '.pdf', '.epub', '.mobi',
    '.zip', '.tar', '.gz', '.bz2', '.xz', '.7z',
    '.rar', '.ar', '.deb', '.rpm', '.pkg',
    '.exe', '.dll', '.so', '.dylib', '.a',
    '.o', '.obj', '.elf', '.bin',
    '.hex', '.srec', '.ihex',
    '.img', '.iso', '.vmdk', '.vdi', '.vhd',
    '.qcow2', '.raw', '.dd',
    '.mp3', '.wav', '.flac', '.aac', '.ogg',
    '.mp4', '.avi', '.mkv', '.mov', '.wmv',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg',
    '.ico', '.cur', '.ani',
    '.psd', '.ai', '.eps', '.indd', '.sketch',
    '.blend', '.3ds', '.max', '.ma', '.mb',
    '.obj', '.fbx', '.dae', '.stl', '.ply',
    '.wrl', '.x3d', '.vrml',
    '.shp', '.kml', '.kmz', '.gpx',
    '.nc', '.hdf', '.h5', '.netcdf',
    '.mat', '.sav', '.rdata', '.rds',
    '.pkl', '.pickle', '.joblib',
    '.parquet', '.avro', '.orc',
    '.arrow', '.feather',
    '.hdf5', '.h5', '.hdf',
    '.fits', '.fit',
    '.mrc', '.rec', '.em',
    '.pdb', '.cif', '.mmcif',
    '.fasta', '.fa', '.fas', '.fna', '.faa',
    '.fastq', '.fq',
    '.sam', '.bam', '.vcf', '.bed',
    '.gtf', '.gff', '.gff3',
    '.phylip', '.nexus', '.newick',
    '.sdf', '.mol', '.pdbqt',
    '.xyz', '.mol2', '.pdb',
    '.gro', '.top', '.itp', '.mdp',
    '.lammps', '.data', '.dump',
    '.vasp', '.poscar', '.contcar',
    '.cif', '.res', '.ins',
    '.crd', '.prmtop', '.parm7',
  }
  
  # Get the file extension
  file_extension = os.path.splitext(file_path)[1].lower()
  
  # Check if the file extension is in our text extensions set
  return file_extension in text_extensions


def count_file_types(directory_path):
  """
  Counts the number of text files and non-text files in a directory.
  
  Args:
    directory_path (str): Path to the directory to analyze
    
  Returns:
    tuple: (text_file_count, non_text_file_count)
    
  Raises:
    FileNotFoundError: If the directory doesn't exist
    PermissionError: If access to the directory is denied
  """
  if not os.path.exists(directory_path):
    raise FileNotFoundError(f"Directory '{directory_path}' does not exist")
  
  if not os.path.isdir(directory_path):
    raise ValueError(f"'{directory_path}' is not a directory")
  
  text_count = 0
  non_text_count = 0
  
  try:
    for filename in os.listdir(directory_path):
      file_path = os.path.join(directory_path, filename)
      
      # Skip directories, only count files
      if os.path.isfile(file_path):
        if is_text_file(file_path):
          text_count += 1
        else:
          non_text_count += 1
          
  except PermissionError:
    raise PermissionError(f"Permission denied accessing directory '{directory_path}'")
  
  return text_count, non_text_count

def is_code_file(file_path):
  """
  Determines if a file is a code file based on its extension.
  
  Args:
    file_path (str): Path to the file to check
    
  Returns:
    bool: True if the file is a code file, False otherwise
  """
  # Define common code file extensions
  code_extensions = {
    # Programming languages
    '.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.hpp', '.cs', '.php',
    '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.dart', '.r', '.m', '.mm',
    '.pl', '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd',
    
    # Web technologies
    '.html', '.htm', '.css', '.scss', '.sass', '.less', '.xml', '.svg',
    '.jsx', '.tsx', '.vue', '.svelte', '.astro',
    
    # Configuration and data formats
    '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.config',
    '.sql', '.sqlite', '.db', '.sqlite3',
    
    # Build and package files
    '.makefile', '.mk', '.cmake', '.gradle', '.pom', '.csproj', '.vcxproj',
    '.sln', '.xcodeproj', '.pbxproj', '.pro', '.pri',
    
    # Documentation and markup
    '.md', '.markdown', '.rst', '.tex', '.latex',
    
    # Shell scripts and automation
    '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd', '.vbs',
    
    # Other common code files
    '.dockerfile', '.dockerignore', '.gitignore', '.gitattributes',
    '.editorconfig', '.eslintrc', '.prettierrc', '.babelrc',
    '.webpack.config.js', '.rollup.config.js', '.vite.config.js',
    '.jest.config.js', '.mocha.opts', '.nycrc', '.browserslistrc'
  }
  
  # Get the file extension
  file_extension = os.path.splitext(file_path)[1].lower()
  
  # Check if the file extension is in our code extensions set
  return file_extension in code_extensions

def get_functions_from_file(repo_name, file_path):
  """
  Extracts function names and their code from a code file.
  
  Args:
    file_path (str): Path to the code file to analyze
    
  Returns:
    list: List of tuples (function_name, function_code) found in the file, empty list if none found
  """
  import ast
  import os
  
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
    # If it's not valid Python, try to extract function names and code using regex
    import re
    
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

def main():
  import sys

  repo_path = sys.argv[1]
  file_path = sys.argv[2]
  
  # file_path = sys.argv[1] if len(sys.argv) > 1 else input("Enter file path: ").strip()
  # file_path = file_path.strip('"\'')
  
  try:
    # functions = get_functions_from_file(repo_name, file_path)
    # print(functions[0][0])
    # print(functions[0][1])
    build_ckg(repo_path)
  except Exception as e:
    print(f"Error: {e}")


if __name__ == "__main__":
  main()