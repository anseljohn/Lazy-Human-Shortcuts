#!/usr/bin/env python3

from pathlib import Path
from lhs.alias import Alias
import lhs.alias_manager as alias_manager

import lhs.paths as paths

import click
import os
import re
import shutil

@click.group()
def cli():
  """Lazy Human Shortcuts - An AI toolkit manager."""
  pass

@cli.command()
def init():
  """Initialize LHS."""
  lhs_dir = paths.get_lhs_dir()

  if os.path.exists(lhs_dir):
    click.echo("LHS has already been initialized.")
    return

  os.makedirs(lhs_dir, exist_ok=True)
  with open(paths.get_aliases_file(), 'w') as f:
    f.write("# LHS aliases\n")
  with open(paths.get_manifest_file(), "w") as f:
    f.write("[]\n")

  zshrc = os.path.expanduser('~/.zshrc')
  alias_line = """
# LHS sourcing
source ~/.lhs/aliases.zsh
function lhs() {
    command lhs "$@"
    if [[ "$1" == "alias" || "$1" == "unalias" ]]; then
        echo " Reloading aliases.zsh..."
        source ~/.zshrc
    fi
}
"""
  with open(zshrc, 'a+') as f:
    f.seek(0)
    f.write(f'\n{alias_line}\n')

  click.echo("LHS has been initialized.")


@cli.command()
def reset():
  """Uninitializes LHS."""
  lhs_dir = paths.get_lhs_dir()
  if not os.path.exists(lhs_dir):
    click.echo("LHS has not been initialized.")
    return
  

  shutil.rmtree(lhs_dir)
  alias_lines = ["# LHS sourcing", "source ~/.lhs/aliases.zsh"]

  zshrc = os.path.expanduser('~/.zshrc')
  with open(zshrc, 'r') as f:
    lines = f.readlines()

  new_lines = [line for line in lines if line not in alias_lines]

  with open(zshrc, 'w+') as f:
    f.writelines(new_lines)
  click.echo("LHS has been reset. Please reinitialize with 'lhs init'.")


@cli.command()
@click.argument('args', nargs=-1)
def alias(args):
  input_str = ' '.join(args)
  match = re.match(r'^(.*?)\s+does\s+(.*)$', input_str)
  if match is None:
    click.echo("Usage: lhs alias \"name\" does \"command\"")
    return

  alias = Alias(match.groups()[0], match.groups()[1])

  # TODO: Create alias validation
  valid = alias.validate()
  if valid:
    alias_manager.save_alias(alias)
  else:
    click.echo("Not nice")

@cli.command()
@click.argument('args', nargs=-1)
def list(args):
  """List aliases/tools."""

  if len(args) == 0:
    click.echo("Usage: lhs list [aliases|tools] [--verbose/-v]")
    return

  verbose = False
  list_aliases = False
  list_tools = False
  for arg in args:
    if arg == "-v" or arg == "--verbose":
      verbose = True
    elif arg == "aliases":
      list_aliases = True
    elif arg == "tools":
      list_tools = True
    else:
      click.echo(f"Unknown argument: {arg}")
      click.echo("Usage: lhs list [aliases|tools] [--verbose/-v]")
      return

  print(f"List aliases: {list_aliases}")
  print(f"List tools: {list_tools}")
  print(f"Verbose: {verbose}")


if __name__ == '__main__':
  cli() 