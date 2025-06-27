# 50% AI
from lhs.llm import embed
from lhs.tool import Tool
from lhs.tool_builder import ToolBuilder

from sklearn.metrics.pairwise import cosine_similarity

import lhs.paths as paths

import json
import numpy
import os

class CommandRegistry:
  def __init__(self):
    with open(paths.get_manifest_file(), 'r') as f:
      self.manifest = json.load(f)

  def embeddings(self):
    embeddings = {}
    for name in self.manifest.keys():
      embeddings[name] = numpy.load(paths.get_embeddings_file(name))
    return embeddings

  def create_tool(self, name, description):
    tool_builder = ToolBuilder()
    tool = tool_builder.build_tool(name, description, Tool.ToolType.ALIAS)
    tool.save()

  def del_tool(self, name):
    # Remove the alias from the aliases file
    aliases_file = paths.get_aliases_file()
    with open(aliases_file, 'r') as f:
      lines = f.readlines()

    filtered_lines = [line for line in lines if f'alias {name}=' not in line]

    with open(aliases_file, 'w') as f:
      f.writelines(filtered_lines)

    tool = Tool.from_dict(name, self.manifest[name])

    # Remove the embedding
    os.remove(paths.get_embeddings_file(name))

    # Remove the script if it's a script
    if tool.type == Tool.ToolType.SCRIPT.value:
      os.remove(tool.script_path)

    # Remove the tool from the manifest
    del self.manifest[tool.name]
    with open(paths.get_manifest_file(), 'w') as f:
      json.dump(self.manifest, f, indent=2)

  def list(self):
    for name in self.manifest.keys():
      tool = Tool.from_dict(name, self.manifest[name])
      print(f"{tool.name} - {tool.type} - {tool.short_description}")

  def find(self, description, top_n=1):
    prompt_emb = embed(description)
    embeddings = self.embeddings()

    sims = []
    for tool_name, emb in embeddings.items():
      sim = cosine_similarity([prompt_emb], [emb])[0][0]
      sims.append((tool_name, sim))

    sims.sort(key=lambda x: x[1], reverse=True)
    return sims[:top_n]
  
  def reset(self):
    for name in list(self.manifest.keys()):
      self.del_tool(name)