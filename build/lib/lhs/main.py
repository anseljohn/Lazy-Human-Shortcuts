#!/usr/bin/env python3

# 50% AI
from lhs.command_registry import CommandRegistry
from lhs.tool import Tool
from lhs.logger import LOG, LogLevel, OUTPUT, DEBUG, INFO, WARNING, ERROR

from openai import OpenAI
from pathlib import Path

import lhs.code_knowledge as code_knowledge
import lhs.paths as paths
import lhs.query_orchestrator as orchestrator 

import click
import os
import time

command_registry = CommandRegistry()

@click.group(invoke_without_command=True)
# @click.argument("query", required=False)
# @click.pass_context
# def cli(ctx, query):
def cli():
  DEBUG("dkawopd")
  # click.echo("Hello, world!")
  # if ctx.invoked_subcommand is None:
  #   if query:
  #     ctx.invoke(run_query, query=query)
  #   else:
  #     click.echo(ctx.get_help())

@cli.command(name="find-tool")  # 👈 This changes the command name
@click.argument('args', nargs=-1)
def find_tool(args):
  OUTPUT("Searching for tool...")
  OUTPUT("Similar tool found:")
  OUTPUT("trainSplats: Trains a splat from a scan and output directory")



# @cli.command()
# @click.argument("query")
# def run_query(query):
#   OUTPUT("Searching for tool...")
#   OUTPUT("NOT FOUND.")
#   OUTPUT("Generating tool...")
#   OUTPUT("Generated tool 'trainSplats' running '~/dev/spatial/bazel-bin/argeo/scaniverse/ScanKit/ScanKit/Neural/TrainSplats $1 --output $2 --useAppPhases'")
  # OUTPUT("Searching 'axolotl-rel' for ae9c4054a13148c7a9d8cb3b4f119316.16...")
  # OUTPUT("Downloading a random scan...")
  # OUTPUT("Downloaded 640b61ef6ead4f93baeec58d583645a2.107_vpsData to ~/Downloads/ae9c4054a13148c7a9d8cb3b4f119316.16/640b61ef6ead4f93baeec58d583645a2.107_vpsData")
  # start_time = time.time()
  
  # INFO(f"Query received: {query}")
  # DEBUG(f"Starting query execution: {query}")
  
  # # Simulate getting an example scan from Google Cloud
  # OUTPUT("Getting the example scan from Google Cloud...")
  # time.sleep(2.5)  # Simulate network delay
  
  # # Simulate preparing the scan for training
  # OUTPUT("Preparing the scan for training...")
  # time.sleep(1.8)  # Simulate processing time
  
  # # Simulate generating splat from scan
  # OUTPUT("Generating splat from scan...")
  # time.sleep(3.2)  # Simulate generation time
  
  # # Generate a fake file path in downloads
  # downloads_path = os.path.expanduser("~/Downloads")
  # splat_filename = f"example_splat.spz"
  # splat_filepath = os.path.join(downloads_path, splat_filename)
  
  # OUTPUT(f"Splat generated at: {splat_filepath}")
  
  # end_time = time.time()
  # runtime_ms = (end_time - start_time) * 1000
  # INFO(f"Query execution completed in {runtime_ms:.2f}ms")

# @cli.command()
# @click.argument("query")
# def run_query(query):
#   start_time = time.time()
  
#   INFO(f"Query received: {query}")
#   DEBUG(f"Starting query execution: {query}")
  
#   # example_call = code_knowledge.get_example_call(query)
#   bash_script = orchestrator.orchestrate(query)
#   import subprocess
#   import sys

#   try:
#     DEBUG(f"Executing bash script: {bash_script}")
#     result = subprocess.run(bash_script, shell=True, capture_output=True, text=True)
#     if result.returncode != 0:
#       if result.stderr:
#         ERROR(f"Command failed with stderr: {result.stderr}")
#       else:
#         ERROR(f"Command failed with return code {result.returncode}")
#     else:
#       DEBUG(f"Command executed successfully with return code {result.returncode}")
#   except Exception as e:
#     ERROR(f"Error executing script: {e}")
    
#   if result.returncode == 0 and result.stdout:
#     from lhs.formatter import format_bash_output
#     INFO("Formatting output...")
#     formatted_output = format_bash_output(query, bash_script, result.stdout)
#     INFO("Output formatting completed")
#     OUTPUT(formatted_output)
  # print(bash_script)
  
  # end_time = time.time()
  # runtime_ms = (end_time - start_time) * 1000
  # INFO(f"Query execution completed in {runtime_ms:.2f}ms")

def create_tool(args, tool_type):
  if len(args) == 0:
    click.echo(f"Usage: lhs {tool_type} \"[name]\" does \"[command/description]\"")
  elif len(args) == 3:
    if args[1] != "does":
      click.echo(f"Usage: lhs {tool_type} \"[name]\" does \"[command/description]\"")
      return

    name = args[0]
    description = args[2]

    INFO(f"Creating {tool_type} tool: {name}")
    command_registry.create_tool(name, description)
    OUTPUT(f"Tool created: {name}")

@cli.command()
@click.argument('args', nargs=-1)
def alias(args):
  """Create an alias.
  Example: 
  $ lhs alias "commit" does "git commit -m"
  $ commit "Add new feature"
  """
  create_tool(args, Tool.ToolType.ALIAS)

@cli.command()
@click.argument('args', nargs=-1)
def script(args):
  """Create a script via prompt.
  Example:
  $ lhs script "backup" does "create a timestamped backup of the current directory"
  $ backup
  """
  create_tool(args, Tool.ToolType.SCRIPT)

@cli.command()
def reset():
  INFO("Resetting command registry")
  command_registry.reset()
  OUTPUT("Command registry reset completed")

@cli.command()
@click.argument('tool_names', nargs=-1)
def remove(tool_names):
  for name in tool_names:
    INFO(f"Removing tool: {name}")
    command_registry.delete_alias(name)
    OUTPUT(f"Tool removed: {name}")

@cli.command()
def list():
  INFO("Listing all tools")
  command_registry.list()

@cli.command()
@click.argument('args', nargs=-1)
def find(args):
  n = 1
  if len(args) == 3:
    if args[0] == "--top":
      n = int(args[1])
      description = args[2]
    elif args[1] == "--top":
      n = int(args[2])
      description = args[0]
    else:
      click.echo("Usage: lhs find \"[description]\" [--top n]")
      click.echo("Default top is 1")
      click.echo("Example: lhs find \"create a new file\" --top 3")
      return
  elif len(args) == 1:
    n = 1
    description = args[0]
  else:
    click.echo("Usage: lhs find \"[description]\" [--top n]")
    click.echo("Default top is 1")
    click.echo("Example: lhs find \"create a new file\" --top 3")
    return
  
  description = args[0]
  INFO(f"Searching for tools matching: {description} (top {n})")
  results = command_registry.find(description, top_n = n)
  OUTPUT(str(results))

# def init():
#   """Initialize LHS."""
#   lhs_dir = paths.get_lhs_dir()

#   if os.path.exists(lhs_dir):
#     click.echo("LHS has already been initialized.")
#     return

#   os.makedirs(lhs_dir, exist_ok=True)
#   with open(paths.get_aliases_file(), 'w') as f:
#     f.write("# LHS aliases\n")
#   with open(paths.get_manifest_file(), "w") as f:
#     f.write("[]\n")

#   zshrc = os.path.expanduser('~/.zshrc')
#   alias_line = """
# # LHS sourcing
# source ~/.lhs/aliases.zsh
# function lhs() {
#     command lhs "$@"
#     if [[ "$1" == "alias" || "$1" == "unalias" ]]; then
#         source ~/.zshrc
#     fi
# }
# """
#   with open(zshrc, 'a+') as f:
#     f.seek(0)
#     f.write(f'\n{alias_line}\n')

#   click.echo("LHS has been initialized.")


# @cli.command()
# def reset():
#   """Uninitializes LHS."""
#   lhs_dir = paths.get_lhs_dir()
#   if not os.path.exists(lhs_dir):
#     click.echo("LHS has not been initialized.")
#     return
  

#   shutil.rmtree(lhs_dir)
#   alias_lines = ["# LHS sourcing", "source ~/.lhs/aliases.zsh"]

#   zshrc = os.path.expanduser('~/.zshrc')
#   with open(zshrc, 'r') as f:
#     lines = f.readlines()

#   new_lines = [line for line in lines if line not in alias_lines]

#   with open(zshrc, 'w+') as f:
#     f.writelines(new_lines)
#   click.echo("LHS has been reset. Please reinitialize with 'lhs init'.")


# @cli.command()
# @click.argument('args', nargs=-1)
# def alias(args):
#   input_str = ' '.join(args)
#   match = re.match(r'^(.*?)\s+does\s+(.*)$', input_str)
#   if match is None:
#     click.echo("Usage: lhs alias \"name\" does \"command\"")
#     return

#   alias = Alias(match.groups()[0], match.groups()[1])

#   # TODO: Create alias validation
#   valid = alias.validate()
#   if valid:
#     alias_manager.save_alias(alias)
#   else:
#     click.echo("Not nice")

# @cli.command()
# @click.argument('args', nargs=-1)
# def tool(args):
#   """Find and build tools"""
#   click.echo(f"Tool: {args}")

# @cli.command()
# @click.argument('args', nargs=-1)
# def list(args):
#   """List aliases/tools."""

#   if len(args) == 0:
#     click.echo("Usage: lhs list [aliases|tools] [--verbose/-v]")
#     return

#   verbose = False
#   list_aliases = False
#   list_tools = False
#   for arg in args:
#     if arg == "-v" or arg == "--verbose":
#       verbose = True
#     elif arg == "aliases":
#       list_aliases = True
#     elif arg == "tools":
#       list_tools = True
#     else:
#       click.echo(f"Unknown argument: {arg}")
#       click.echo("Usage: lhs list [aliases|tools] [--verbose/-v]")
#       return

#   print(f"List aliases: {list_aliases}")
#   print(f"List tools: {list_tools}")
#   print(f"Verbose: {verbose}")


if __name__ == '__main__':
  cli() 