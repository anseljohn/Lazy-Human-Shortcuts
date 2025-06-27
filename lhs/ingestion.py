from lhs.llm import prompt, embed, LLMOpts
from pathlib import Path

import lhs.paths as paths
import lhs.system_prompts as system_prompts

import json
import numpy
import os
import re
import sys

def has_main_function(file_path):
  """Check if a file contains an int main function."""
  try:
    with open(file_path, 'r', encoding='utf-8') as f:
      content = f.read()
      # Look for int main with various patterns
      patterns = [
        r'int\s+main\s*\(',
        r'int\s+main\s*\([^)]*\)',
        r'int\s+main\s*\([^)]*\)\s*{',
      ]
      return any(re.search(pattern, content) for pattern in patterns)
  except (UnicodeDecodeError, IOError):
    # Skip files that can't be read as text
    return False
  
def io(file_path):
  """Uses openai to read the file and determine its input and output"""
  with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

  return prompt(system_prompts.CODE_IO, f"File name:{file_path}\nCode:{content}", LLMOpts())


def write_codebase_metadata(directory):
  """Write code metadata"""
  
  # Common source file extensions that can have main functions
  source_extensions = {'.cpp', '.c', '.cc', '.cxx', '.c++', '.C'}
  
  for root, dirs, files in os.walk(directory):
    for file in files:
      file_path = Path(root) / file
      file_ext = file_path.suffix.lower()
      
      # Check if it's a source file
      if file_ext in source_extensions:
        if has_main_function(file_path):
          file_metadata = json.loads(io(file_path))
          
          # Add the code_path to the metadata
          file_metadata['code_path'] = str(file_path)

          # Make all directories relative to file_path
          metadata_file = paths.get_code_metadata_file(directory, file_path)
          
          # Ensure the parent directory exists
          metadata_file = Path(metadata_file)
          metadata_file.parent.mkdir(parents=True, exist_ok=True)
          with open(metadata_file, 'w') as f:
            json.dump(file_metadata, f, indent=2)

def write_codebase_embeddings():
  """Write embeddings for all metadata files in the codebase metadata directory"""
  codebase_metadata_dir = paths.get_codebase_metadata_dir()
  
  # Walk through all files in the codebase metadata directory
  for root, dirs, files in os.walk(codebase_metadata_dir):
    for file in files:
      if file.endswith('.json'):
        metadata_file_path = Path(root) / file
        
        # Read the metadata
        with open(metadata_file_path, 'r') as f:
          metadata = json.load(f)
        
        # Create embedding text from metadata
        emb_text = f"{metadata.get('description', '')}. Inputs: {','.join(metadata.get('input_tags', []))}. Outputs: {','.join(metadata.get('output_tags', []))}"
        
        # Generate embedding
        embedding = embed(emb_text)
        
        # Save embedding to file
        embedding_file = paths.get_code_embeddings_file(str(metadata_file_path))
        
        numpy.save(embedding_file, embedding)
  

if __name__ == "__main__":
  
  if len(sys.argv) != 2:
    sys.exit(1)
  
  directory = sys.argv[1]
  
  codebase_metadata_dir = paths.get_codebase_metadata_dir()
  
  if not os.path.exists(codebase_metadata_dir):
    os.makedirs(codebase_metadata_dir, exist_ok=True)
    
  write_codebase_metadata(directory)
  write_codebase_embeddings()