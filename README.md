# LHS - Lazy Human Shortcuts

A simple command-line tool to manage zsh aliases permanently.

## Installation

### Method 1: Using the install script
```bash
./install.sh
```

### Method 2: Manual installation with pip
```bash
pip install -e .
```

### Method 3: Install from source
```bash
python setup.py install
```

## Usage

```bash
lhs alias <name> does <command>
lhs list
lhs remove <alias>
```

### Examples

```bash
# Add an alias
lhs alias hello does "echo 'hello world'"

# List all aliases
lhs list

# Remove an alias
lhs remove hello
```

## How it works

- Creates a `.lhs` directory in your home folder
- Stores all aliases in `~/.lhs/aliases`
- Automatically adds a source line to your `~/.zshrc` file
- Manages aliases without cluttering your `.zshrc`

## Development

### Project structure
```
lhs/
├── python/
│   ├── __init__.py
│   └── main.py
├── lhs (executable script)
├── setup.py
├── requirements.txt
├── install.sh
└── README.md
```

### Testing locally
```bash
# Direct execution during development
./lhs alias test does "echo test"
./lhs list
./lhs remove test

# Or using Python module
PYTHONPATH=python python -m main alias test does "echo test"
``` 