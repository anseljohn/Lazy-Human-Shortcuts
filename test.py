#!/usr/bin/env python3
"""
CodeLlama ZSH Code Generator
A script that uses CodeLlama to generate zsh commands from natural language prompts.
"""

import requests
import json
import sys
import argparse


def generate_zsh_code(prompt, model_url="http://localhost:11434", model_name="codellama"):
    """
    Generate zsh code using CodeLlama via Ollama API
    
    Args:
        prompt (str): Natural language description of what you want to do
        model_url (str): URL where Ollama is running
        model_name (str): Name of the CodeLlama model to use
    
    Returns:
        str: Generated zsh code
    """
    
    # Craft a specific prompt for zsh code generation
    system_prompt = """You are an expert in zsh shell scripting. Generate clean, efficient zsh code based on the user's request. 
Only return the zsh code without explanations or markdown formatting. Focus on best practices and modern zsh features."""
    
    full_prompt = f"{system_prompt}\n\nUser request: {prompt}\n\nZsh code:"
    
    # Prepare the request payload
    payload = {
        "model": model_name,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,  # Low temperature for more deterministic code
            "top_p": 0.9,
            "max_tokens": 500
        }
    }
    
    try:
        # Make request to Ollama API
        response = requests.post(
            f"{model_url}/api/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Extract and clean the generated code
        generated_code = result.get("response", "").strip()
        
        # Remove any markdown code blocks if present
        if generated_code.startswith("```"):
            lines = generated_code.split('\n')
            generated_code = '\n'.join(lines[1:-1]) if len(lines) > 2 else generated_code
        
        return generated_code
        
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {e}"
    except json.JSONDecodeError as e:
        return f"Error parsing response: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="Generate zsh code using CodeLlama",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python codellama_zsh.py "find all .py files modified in the last 7 days"
  python codellama_zsh.py "create a backup of my home directory excluding hidden files"
  python codellama_zsh.py --interactive
        """
    )
    
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Natural language description of what you want to do"
    )
    
    parser.add_argument(
        "--model-url",
        default="http://localhost:11434",
        help="URL where Ollama is running (default: http://localhost:11434)"
    )
    
    parser.add_argument(
        "--model",
        default="codellama",
        help="CodeLlama model name (default: codellama)"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )
    
    args = parser.parse_args()
    
    if args.interactive:
        print("CodeLlama ZSH Generator (Interactive Mode)")
        print("Type 'quit' or 'exit' to stop\n")
        
        while True:
            try:
                prompt = input("zsh> ").strip()
                if prompt.lower() in ['quit', 'exit', 'q']:
                    break
                if not prompt:
                    continue
                    
                print("Generating zsh code...")
                result = generate_zsh_code(prompt, args.model_url, args.model)
                print(f"\n{result}\n")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
                
    elif args.prompt:
        print("Generating zsh code...")
        result = generate_zsh_code(args.prompt, args.model_url, args.model)
        print(result)
        
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()