# 100% AI
from pathlib import Path

import os

def get_lhs_dir():
  return os.path.expanduser("~/.lhs")

def get_log_file():
  return os.path.join(get_lhs_dir(), "debug.log")

def get_command_registry_dir():
  return os.path.join(get_lhs_dir(), "registry")

def get_manifest_file():
  return os.path.join(get_lhs_dir(), "manifest.json")

def get_aliases_file():
  return os.path.join(get_lhs_dir(), "aliases.zsh")

def get_scripts_dir():
  return os.path.join(get_lhs_dir(), "scripts")

def get_script_path(name: str):
  return os.path.join(get_scripts_dir(), f"{name}.sh")

def get_embeddings_file(name: str):
  return os.path.join(get_lhs_dir(), "embeddings",f"{name}.npy")

def get_codebase_metadata_dir():
  return os.path.join(get_lhs_dir(), "codebase_metadata")

def get_code_metadata_file(codebase_dir: str, codebase_relative_path: str):
  codebase_dir = Path(codebase_dir)
  codebase_relative_path = Path(codebase_relative_path)
  relative_path = codebase_relative_path.relative_to(codebase_dir)
  return os.path.join(get_codebase_metadata_dir(), relative_path.with_suffix('.json'))

def get_code_embeddings_file(metadata_file_path: str):
  return Path(metadata_file_path).with_suffix(".npy")