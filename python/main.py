#!/usr/bin/env python3
"""
LHS - Lazy Human Shortcuts
A simple tool to manage zsh aliases permanently
"""

import sys
import os
import re
import subprocess
from pathlib import Path


def get_lhs_dir():
    """Get the path to the .lhs directory"""
    home = Path.home()
    lhs_dir = home / ".lhs"
    return lhs_dir


def get_aliases_file():
    """Get the path to the aliases file"""
    return get_lhs_dir() / "aliases"


def get_zshrc_path():
    """Get the path to the user's .zshrc file"""
    home = Path.home()
    zshrc_path = home / ".zshrc"
    return zshrc_path


def create_shell_wrapper():
    """Create a shell function wrapper for lhs that can reload aliases"""
    lhs_dir = get_lhs_dir()
    wrapper_file = lhs_dir / "lhs_wrapper.sh"
    aliases_file = get_aliases_file()
    
    wrapper_content = f'''#!/bin/zsh
# LHS shell wrapper for automatic alias reloading

lhs_wrapper() {{
    # Call the actual lhs python command
    command lhs "$@"
    
    # If the command was alias or remove, reload aliases
    if [[ "$1" == "alias" || "$1" == "remove" ]]; then
        if [[ -f "{aliases_file}" ]]; then
            source "{aliases_file}"
        fi
    fi
}}

# Make lhs an alias to our wrapper function
alias lhs='lhs_wrapper'
'''
    
    with open(wrapper_file, 'w') as f:
        f.write(wrapper_content)
    
    return wrapper_file


def setup_lhs_directory():
    """Create the .lhs directory and aliases file if they don't exist"""
    lhs_dir = get_lhs_dir()
    aliases_file = get_aliases_file()
    
    # Create .lhs directory
    if not lhs_dir.exists():
        lhs_dir.mkdir(exist_ok=True)
    
    # Create aliases file with header if it doesn't exist
    if not aliases_file.exists():
        with open(aliases_file, 'w') as f:
            f.write("# LHS aliases\n\n")
    
    return aliases_file


def ensure_zshrc_sources_aliases():
    """Ensure .zshrc sources our aliases file and wrapper"""
    zshrc_path = get_zshrc_path()
    aliases_file = get_aliases_file()
    wrapper_file = create_shell_wrapper()
    
    # Create .zshrc if it doesn't exist
    if not zshrc_path.exists():
        zshrc_path.touch()
    
    # Read existing .zshrc content
    with open(zshrc_path, 'r') as f:
        zshrc_content = f.read()
    
    # Check if our source lines already exist
    aliases_source_line = f"source {aliases_file}"
    wrapper_source_line = f"source {wrapper_file}"
    
    lines_to_add = []
    
    if aliases_source_line not in zshrc_content:
        lines_to_add.append(aliases_source_line)
    
    if wrapper_source_line not in zshrc_content:
        lines_to_add.append(wrapper_source_line)
    
    if lines_to_add:
        # Add source lines to .zshrc
        with open(zshrc_path, 'a') as f:
            f.write("\n# LHS - Auto-reload aliases\n")
            for line in lines_to_add:
                f.write(f"{line}\n")
        return True
    
    return False


def add_alias_to_file(alias_name, command):
    """Add an alias to the aliases file"""
    aliases_file = setup_lhs_directory()
    
    # Read existing content
    with open(aliases_file, 'r') as f:
        existing_content = f.read()
    
    # Check if alias already exists
    alias_pattern = rf"^alias {re.escape(alias_name)}="
    if re.search(alias_pattern, existing_content, re.MULTILINE):
        response = input(f"Alias '{alias_name}' exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            return
        
        # Remove existing alias
        lines = existing_content.split('\n')
        filtered_lines = []
        for line in lines:
            if not re.match(alias_pattern, line):
                filtered_lines.append(line)
        existing_content = '\n'.join(filtered_lines)
    
    # Prepare the new alias line
    alias_line = f"alias {alias_name}=\"{command}\""
    
    # Add alias to the file
    with open(aliases_file, 'w') as f:
        f.write(existing_content)
        if existing_content and not existing_content.endswith('\n'):
            f.write('\n')
        f.write(f"{alias_line}\n")
    
    # Ensure .zshrc sources our aliases file and wrapper
    zshrc_updated = ensure_zshrc_sources_aliases()
    
    print(f"Added: {alias_name}")
    
    if zshrc_updated:
        print("Restart terminal to enable auto-reload")


def add_prompt_alias(alias_name, prompt):
    """Handle prompt-based alias creation (placeholder for LLM integration)"""
    print(f"Prompt alias '{alias_name}': {prompt}")
    print("Not implemented yet")


def remove_alias_from_file(alias_name):
    """Remove an alias from the aliases file"""
    aliases_file = get_aliases_file()
    
    if not aliases_file.exists():
        print("No aliases found")
        return
    
    # Read existing content
    with open(aliases_file, 'r') as f:
        existing_content = f.read()
    
    # Check if alias exists
    alias_pattern = rf"^alias {re.escape(alias_name)}="
    if not re.search(alias_pattern, existing_content, re.MULTILINE):
        print(f"Alias '{alias_name}' not found")
        return
    
    # Remove the alias
    lines = existing_content.split('\n')
    filtered_lines = []
    
    for line in lines:
        if not re.match(alias_pattern, line):
            filtered_lines.append(line)
    
    # Write back the content without the removed alias
    new_content = '\n'.join(filtered_lines)
    new_content = re.sub(r'\n\n+', '\n\n', new_content)
    
    with open(aliases_file, 'w') as f:
        f.write(new_content)
    
    print(f"Removed: {alias_name}")


def list_aliases():
    """List all current aliases managed by lhs"""
    aliases_file = get_aliases_file()
    
    if not aliases_file.exists():
        print("No aliases found")
        return
    
    with open(aliases_file, 'r') as f:
        content = f.read()
    
    # Extract alias lines
    alias_lines = []
    for line in content.split('\n'):
        if line.strip() and line.startswith('alias ') and not line.startswith('#'):
            alias_lines.append(line.strip())
    
    if not alias_lines:
        print("No aliases found")
    else:
        for alias_line in alias_lines:
            print(alias_line)


def parse_command(args):
    """Parse the lhs command arguments"""
    if len(args) < 2:
        return None, None, None
    
    if args[1] == "list":
        return "list", None, None
    
    if args[1] == "remove":
        if len(args) < 3:
            print("Usage: lhs remove <alias>")
            sys.exit(1)
        
        alias_name = args[2]
        # Remove quotes if present
        if alias_name.startswith('"') and alias_name.endswith('"'):
            alias_name = alias_name[1:-1]
        
        return "remove", alias_name, None
    
    if args[1] == "alias":
        if len(args) < 5:
            print("Usage: lhs alias <name> does <command>")
            print("       lhs alias <name> prompt <description>")
            print("       lhs list")
            print("       lhs remove <alias>")
            sys.exit(1)
        
        alias_name = args[2]
        action_word = args[3]
        content = args[4]
        
        # Remove quotes if present
        if alias_name.startswith('"') and alias_name.endswith('"'):
            alias_name = alias_name[1:-1]
        if content.startswith('"') and content.endswith('"'):
            content = content[1:-1]
        
        if action_word == "does":
            return "alias", alias_name, content
        elif action_word == "prompt":
            return "prompt", alias_name, content
        else:
            print("Error: Third argument must be 'does' or 'prompt'")
            print("Usage: lhs alias <name> does <command>")
            print("       lhs alias <name> prompt <description>")
            sys.exit(1)
    
    # If we get here, invalid command
    print("Usage: lhs alias <name> does <command>")
    print("       lhs alias <name> prompt <description>")
    print("       lhs list")
    print("       lhs remove <alias>")
    sys.exit(1)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: lhs alias <name> does <command>")
        print("       lhs alias <name> prompt <description>")
        print("       lhs list")
        print("       lhs remove <alias>")
        sys.exit(1)
    
    try:
        action, alias_name, content = parse_command(sys.argv)
        
        if action == "list":
            list_aliases()
        elif action == "alias":
            add_alias_to_file(alias_name, content)
        elif action == "prompt":
            add_prompt_alias(alias_name, content)
        elif action == "remove":
            remove_alias_from_file(alias_name)
        else:
            print("Invalid command")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 