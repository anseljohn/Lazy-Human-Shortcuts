import lhs.paths as paths
import lhs.semantics as semantics
import lhs.alias_manager as alias_manager

import json

def load_manifest():
  with open(paths.get_manifest_file(), 'r') as f:
    return json.load(f)

class Alias:
  def __init__(self, name, command):
    self.name = name
    self.command = command
    self.description = semantics.describe_command(name, command)

  def validate(self):
    return True
  
  def to_json(self):
    return {
      "name": self.name,
      "command": self.command,
      "description": self.description
    }
  
  # def save(self):
  #   manifest = load_manifest()
  #   self_json = {
  #     "name": self.name,
  #     "command": self.command,
  #     "description": self.description
  #   }
  #   manifest.append(self_json)

  #   with open(paths.get_manifest_file(), 'w') as f:
  #     json.dump(manifest, f)

  #   alias_line = f"alias {self.name}='{self.command}'"
  #   with open(paths.get_aliases_file(), 'w') as f:
  #     f.seek(0)
  #     f.write(f"\n{alias_line}\n")

