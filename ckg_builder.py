'''
Builds a code knowledge graph (CKG) from a repository.

Performs three traversals:

1. Initial traversal of the repository
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
import os
from pathlib import Path
from typing import Union

from ckg_node import CKGNode
from code_parser import get_functions
from file_utils import infer_file_type


class CKGBuilder:
  def __init__(self, repo_path: Union[str, Path]):
    if isinstance(repo_path, str):
      repo_path = Path(repo_path)

    self.repo_name = os.path.basename(repo_path)
    self.repo_path = repo_path


  def build_function_node(self, parent_node, function_name, function_code):
    return CKGNode(
      uid = f"{parent_node.uid}::{function_name}",
      type = "function",
      name = function_name,
      content = function_code
    )


  def build_file_node(self, file_path: Path):
    file_node = CKGNode(
      uid = f"{self.repo_name}/{os.path.relpath(file_path, self.repo_path)}",
      type = "file",
      name = os.path.basename(file_path))

    if infer_file_type(file_path) == "code":
      functions = get_functions(file_path)
      for function in functions:
        function_node = self.build_function_node(file_node, function[0], function[1])
        file_node.add_child(function_node)

    return file_node


  def build_folder_node(self, path: Path) -> CKGNode:
    dir_node = CKGNode(
      uid = f"{self.repo_name}/{os.path.relpath(path, self.repo_path)}",
      type = "folder",
      name = os.path.basename(path))

    for item in os.listdir(path):
      item_node = self.build_node(path.joinpath(item))
      dir_node.add_child(item_node)

    return dir_node


  def build_node(self, path: Path) -> CKGNode:
    if path.is_file():
      return self.build_file_node(path)
    elif path.is_dir():
      return self.build_folder_node(path)
    else:
      raise ValueError(f"Invalid path: {path}")


  def build_ckg(self):
    repo_node = self.build_node(self.repo_path)
    repo_node.uid = self.repo_name
    repo_node.type = "repo"

    return repo_node