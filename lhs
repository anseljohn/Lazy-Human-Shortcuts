#!/usr/bin/env python3
import sys
from pathlib import Path

# Add the python directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir / "python"))

# Import and run the main function
from main import main, get_lhs_dir

def check_wrapper_setup():
    """Check if the wrapper is set up and inform user"""
    lhs_dir = get_lhs_dir()
    wrapper_file = lhs_dir / "lhs_wrapper.sh"
    
    if wrapper_file.exists():
        print("Note: For auto-reload, source the wrapper:")
        print(f"source {wrapper_file}")
        print("Or restart your terminal if already sourced in .zshrc")

if __name__ == "__main__":
    # Check if this is an alias or remove command
    is_alias_command = len(sys.argv) > 1 and sys.argv[1] in ['alias', 'remove']
    
    # Run the main function
    main()
    
    # If it was an alias or remove command, remind about wrapper
    if is_alias_command:
        check_wrapper_setup() 