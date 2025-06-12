#!/bin/bash

# LHS Installation Script
echo "Installing LHS (Lazy Human Shortcuts)..."

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "Error: pip is not available. Please install pip first."
    exit 1
fi

# Install the package in development mode
pip install -e .

if [ $? -eq 0 ]; then
    echo "LHS installed successfully!"
    echo "You can now use 'lhs' from anywhere in your terminal."
    echo ""
    echo "Usage: lhs alias <name> does <command>"
    echo "       lhs list"
    echo "       lhs remove <alias>"
else
    echo "Installation failed. Please check the error messages above."
    exit 1
fi 