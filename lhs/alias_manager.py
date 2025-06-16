import lhs.paths as paths

import json

def load_manifest():
  with open(paths.get_manifest_file(), 'r') as f:
    return json.load(f)

def save_alias(alias):
  manifest = load_manifest()
  manifest.append(alias.to_json())

  # Save to manifest
  with open(paths.get_manifest_file(), 'w') as f:
    json.dump(manifest, f)
  
  # Save to aliases file
  alias_line = f"alias {alias.name}='{alias.command}'"
  with open(paths.get_aliases_file(), 'w') as f:
    f.seek(0)
    f.write(f"\n{alias_line}\n")
  
  