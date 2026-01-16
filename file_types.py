# file_types.py

from typing import Dict, Set

# Mapping from file extensions to high-level file types
EXTENSION_TO_TYPE: Dict[str, str] = {
    # Code
    ".py": "code",
    ".js": "code",
    ".ts": "code",
    ".tsx": "code",
    ".jsx": "code",
    ".java": "code",
    ".cpp": "code",
    ".c": "code",
    ".cs": "code",
    ".rb": "code",
    ".go": "code",
    ".rs": "code",
    ".swift": "code",
    ".kt": "code",

    # Config
    ".json": "config",
    ".yaml": "config",
    ".yml": "config",
    ".toml": "config",
    ".ini": "config",
    ".env": "config",

    # Text/Docs
    ".md": "text",
    ".txt": "text",
    ".rst": "text",

    # Data
    ".csv": "data",
    ".tsv": "data",
    ".parquet": "data",
    ".xls": "data",
    ".xlsx": "data",

    # Images (skip or compress)
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".webp": "image",
    ".svg": "image",
    ".gif": "image",

    # Binaries
    ".exe": "binary",
    ".dll": "binary",
    ".so": "binary",
    ".zip": "binary",
    ".jar": "binary",
    ".pkl": "binary"
}

# Optional: per-type metadata and processing rules
FILE_TYPE_RULES: Dict[str, Dict] = {
    "code": {
        "parseable": True,
        "summarizable": True,
        "include_in_context": True,
        "priority": 1
    },
    "config": {
        "parseable": True,
        "summarizable": False,   # you could summarize if you want, but it's often too verbose
        "include_in_context": True,
        "priority": 3
    },
    "text": {
        "parseable": True,
        "summarizable": True,
        "include_in_context": True,
        "priority": 2
    },
    "data": {
        "parseable": False,
        "summarizable": False,
        "include_in_context": False,
        "priority": 99
    },
    "image": {
        "parseable": False,
        "summarizable": False,
        "include_in_context": False,
        "priority": 99
    },
    "binary": {
        "parseable": False,
        "summarizable": False,
        "include_in_context": False,
        "priority": 100
    },
    "unknown": {
        "parseable": False,
        "summarizable": False,
        "include_in_context": False,
        "priority": 100
    }
}
