import os
import sys
from re import A
from ckg_node import CKGNode
from ckg_builder import CKGBuilder


def main():
  import sys

  repo_path = sys.argv[1]
  file_path = sys.argv[2]

  try:
    builder = CKGBuilder(repo_path)
    builder.build_ckg()
  except Exception as e:
    print(f"Error: {e}")


if __name__ == "__main__":
  main()