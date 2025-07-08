'''
Builds a code knowledge graph (CKG) from a repository.

Performs three traversals:

1. Breadth first traversal of the repository
- Adds nodes to the base CKG
- Nodes consist of a function, file, or directory with bidirectional links to
  their parent and children
- The root node is the repository
- A local context is added to leaf nodes using the contents of 
  the file or function body

2. Depth first traversal of the CKG (non-leaf local context propagation)
- Adds local context to the non-leaf nodes
- Local context is added by looking at the local context of the node's children

3. Breadth first traversal of the CKG (global context propagation)
- Enriches the CKG with global context
- Global context is added by looking at the node, its parent, and its local context
- This captures broader semantic understanding from repo-level intent down to specific code regions
'''

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
