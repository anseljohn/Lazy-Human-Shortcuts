import os

def get_lhs_dir():
  return os.path.expanduser("~/.lhs")

def get_aliases_file():
  return os.path.join(get_lhs_dir(), "aliases.zsh")

def get_manifest_file():
  return os.path.join(get_lhs_dir(), "manifest.json")
