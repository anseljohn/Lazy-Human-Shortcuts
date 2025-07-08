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

from ckg_node import CKGNode
from collections import deque
from file_utils import infer_file_type
from pathlib import Path
import os

class CKGBuilder:
  def __init__(self, repo_path):
    self.repo_name = os.path.basename(repo_path)
    self.repo_path = repo_path

  def traverse(self, path: str) -> CKGNode:
    dir_node = CKGNode(
      uid = f"{self.repo_name}/{os.path.relpath(path, self.repo_path)}",
      type = "folder",
      name = os.path.basename(path))
    
    for item in os.listdir(path):
      item_path = os.path.join(path, item)
      if os.path.isfile(item_path):
        file_node = CKGNode(
          uid = f"{self.repo_name}/{os.path.relpath(item_path, self.repo_path)}",
          type = "file",
          name = os.path.basename(item_path))

        file_type = infer_file_type(item_path)
        # print(f"uid: {file_node.uid}, file type: {file_type}")

        file_node.owner = dir_node 
        dir_node.children.append(file_node)
      elif os.path.isdir(item_path):
        child_folder_node = self.traverse(item_path)
        child_folder_node.owner = dir_node
        dir_node.children.append(child_folder_node)

    return dir_node

  def build(self):
    repo_node = self.traverse(self.repo_path)

    # for child in repo_node.children:
    #   if child.type == "folder":
    #     print(child.children)