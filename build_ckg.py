
from CKGNode import CKGNode
from collections import deque

import os

def traverse_directory(repo_name, repo_path):
  
  queue = deque([(repo_path, 0)])
  
  while queue:
    current_path, level = queue.popleft()
    
    indent = "  " * level
    
    try:
      items = os.listdir(current_path)
      
      files = []
      directories = []
      
      for item in items:
        item_path = os.path.join(current_path, item)
        if os.path.isfile(item_path):
          files.append(item)
        elif os.path.isdir(item_path):
          directories.append(item)

      for directory in directories:
        print(f"{indent}{directory}")
        queue.append((os.path.join(current_path, directory), level + 1))
      
      for file in files:
        print(f"{indent}{file}")
      
      return
        
    except PermissionError:
      print(f"{indent}Permission denied: {current_path}")
    except Exception as e:
      print(f"{indent}Error accessing {current_path}: {e}")

def build_ckg(repo_path):
  repo_name = os.path.basename(repo_path)
  
  repo_node = CKGNode(
    uid = repo_name, 
    type = "repo",
    name = repo_name)

  traverse_directory(repo_name, repo_path)
