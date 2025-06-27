# 75% AI
from lhs.llm import prompt, embed, LLMOpts
from lhs.tool import Tool
from openai import OpenAI

import lhs.paths as paths
import lhs.system_prompts as system_prompts
import lhs.vars as vars

import ast
import json
import shlex
import shutil

def is_shell_cmd(cmd: str) -> bool:
  try:
    tokens = shlex.split(cmd)
    if not tokens:
      return False
    cmd_base = tokens[0]
    return shutil.which(cmd_base) is not None
  except Exception:
    return False
  
class ToolBuilder:
  def __init__(self) -> Tool:
    pass

  def build_tool(self, name: str, description: str, tool_type):
    code = None
    if tool_type == Tool.ToolType.ALIAS:
      code = description
    else:
      code = prompt(system_prompts.TOOL_GEN,
                             f"Name: {name}\nDescription: {description}",
                             LLMOpts())

    opts = LLMOpts()
    opts.temperature = 0.0
    opts.max_tokens = 400
    metadata_str = prompt(system_prompts.DESCRIPTION_GEN,
                                   f"Name: {name}\nDescription: {description}\nCode: {code}",
                                   opts)
    
    try:
      metadata = json.loads(metadata_str)
    except json.JSONDecodeError:
      metadata = ast.literal_eval(metadata_str)

    command = None
    script_path = None
    match tool_type:
      case Tool.ToolType.ALIAS:
        command = code
      case Tool.ToolType.SCRIPT:
        script_path = paths.get_script_path(name)
        command = f"{script_path}"
      case _:
        raise ValueError(f"Invalid tool type: {tool_type}")
      
    tool = Tool(
      name=name,
      type=tool_type,
      short_description=metadata["short_description"],
      long_description=metadata["long_description"],
      command=command,
      code=code,
      script_path=script_path,
      input_tags=metadata["input_tags"],
      output_tags=metadata["output_tags"],
      tags=metadata["tags"]
    )

    emb_text = f"{tool.short_description}. Inputs: {",".join(tool.input_tags)}. Outputs: {",".join(tool.output_tags)}"
    emb = embed(emb_text)

    tool.embedding = emb
      
    return tool
