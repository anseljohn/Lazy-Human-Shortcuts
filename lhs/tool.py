# 
from dataclasses import asdict, dataclass, field
from enum import Enum

import lhs.paths as paths

import json
import numpy

@dataclass
class Tool:
  class ToolType(Enum):
    ALIAS = "alias"
    SCRIPT = "script"
    name: str

  name: str
  type: ToolType
  short_description: str
  long_description: str
  command: str
  code: str
  script_path: str
  input_tags: list[str] = field(default_factory=list)
  output_tags: list[str] = field(default_factory=list)
  tags: list[str] = field(default_factory=list)
  embedding: list[float] = field(default_factory=list)

  def to_dict(self):
    data = asdict(self)

    # Add type to data
    data["type"] = self.type.value

    # Remove code from data, if it's a script it's in the script_path
    del data["code"]

    # Remove embedding from data, it's in the file
    del data["embedding"]

    return data
  
  @classmethod
  def from_dict(cls, name, data):
    data["type"] = Tool.ToolType(data["type"])
    data["code"] = None
    data["embedding"] = numpy.load(paths.get_embeddings_file(name))
    tool = cls(**data)
    tool.name = name
    return tool
  
  def save(self):
    # Save the tool alias
    with open(paths.get_aliases_file(), "a") as f:
      f.write(f"alias {self.name}=\"{self.command}\"\n")

    # Save the tool script
    if self.type == Tool.ToolType.SCRIPT:
      with open(self.script_path, "w") as f:
        f.write(self.code)

    # Save the embedding
    numpy.save(paths.get_embeddings_file(self.name), numpy.array(self.embedding, dtype=numpy.float32))

    # Save the tool to the manifest
    with open(paths.get_manifest_file(), "r") as f:
      manifest = json.load(f)
    
    manifest[self.name] = self.to_dict()

    with open(paths.get_manifest_file(), "w") as f:
      json.dump(manifest, f, indent=2)