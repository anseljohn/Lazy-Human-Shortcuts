# 100% AI
import os
import json
import re
from pathlib import Path
from typing import Dict, List, Set

class CodeGraphBuilder:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.graph: Dict[str, List[str]] = {}
        self.processed_files: Set[str] = set()
        
        # Common include patterns for different languages
        self.include_patterns = {
            'python': r'^(?:from\s+(\S+)\s+import|import\s+(\S+))',
            'cpp': r'#include\s+[<"]([^>"]+)[>"]',
            'c': r'#include\s+[<"]([^>"]+)[>"]',
            'rust': r'use\s+(\S+)',
            'javascript': r'import\s+(?:.*?from\s+)?[\'"]([^\'"]+)[\'"]',
            'typescript': r'import\s+(?:.*?from\s+)?[\'"]([^\'"]+)[\'"]',
        }

    def _get_file_type(self, file_path: str) -> str:
        """Determine the file type based on extension."""
        ext = file_path.lower().split('.')[-1]
        if ext in ['py']:
            return 'python'
        elif ext in ['cpp', 'hpp']:
            return 'cpp'
        elif ext in ['c', 'h']:
            return 'c'
        elif ext in ['rs']:
            return 'rust'
        elif ext in ['js']:
            return 'javascript'
        elif ext in ['ts', 'tsx']:
            return 'typescript'
        return 'unknown'

    def _parse_includes(self, file_path: str) -> List[str]:
        """Parse include statements from a file."""
        includes = []
        file_type = self._get_file_type(file_path)
        
        if file_type not in self.include_patterns:
            return includes

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            pattern = self.include_patterns[file_type]
            matches = re.finditer(pattern, content, re.MULTILINE)
            
            for match in matches:
                include = match.group(1)
                if include:
                    includes.append(include)
                    
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            
        return includes

    def _normalize_path(self, file_path: str) -> str:
        """Normalize file path to be relative to root directory."""
        return str(Path(file_path).relative_to(self.root_dir))

    def build_graph(self) -> Dict[str, List[str]]:
        """Build the code graph by recursively processing all files."""
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = self._normalize_path(file_path)
                
                if rel_path in self.processed_files:
                    continue
                    
                self.processed_files.add(rel_path)
                includes = self._parse_includes(file_path)
                
                if includes:
                    self.graph[rel_path] = includes
                    
        return self.graph

    def save_graph(self, output_file: str):
        """Save the code graph to a JSON file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.graph, f, indent=2)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Build a code graph from include statements')
    parser.add_argument('directory', help='Root directory to scan')
    parser.add_argument('--output', '-o', default='code_graph.json',
                      help='Output JSON file (default: code_graph.json)')
    
    args = parser.parse_args()
    
    builder = CodeGraphBuilder(args.directory)
    graph = builder.build_graph()
    builder.save_graph(args.output)
    
    print(f"Code graph built successfully! Found {len(graph)} files with dependencies.")
    print(f"Graph saved to {args.output}")

if __name__ == '__main__':
    main()
