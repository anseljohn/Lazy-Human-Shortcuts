#!/usr/bin/env python3
"""
CodeLlama ZSH Alias/Function Generator
A script that uses CodeLlama to generate zsh aliases or functions from natural language prompts.
"""

import requests
import json
import sys
import argparse


def check_ollama_status(model_url):
    """Check if Ollama is running and what models are available"""
    try:
        # Check if Ollama is running
        response = requests.get(f"{model_url}/api/tags", timeout=5)
        response.raise_for_status()
        models = response.json().get("models", [])
        return True, [model["name"] for model in models]
    except Exception as e:
        return False, str(e)


def generate_zsh_code(alias_name, prompt, model_url="http://localhost:11434", model_name="codellama"):
    """
    Generate zsh alias or function using CodeLlama via Ollama API
    
    Args:
        alias_name (str): Name for the alias or function
        prompt (str): Natural language description of what you want to do
        model_url (str): URL where Ollama is running
        model_name (str): Name of the CodeLlama model to use
    
    Returns:
        str: Generated zsh alias or function
    """
    
    # First check if Ollama is running
    is_running, info = check_ollama_status(model_url)
    if not is_running:
        return f"""Ollama is not running or not accessible at {model_url}
        
Troubleshooting steps:
1. Start Ollama: 'ollama serve' (or just 'ollama' on some systems)
2. Check if it's running: 'ps aux | grep ollama'
3. Test connection: 'curl {model_url}/api/tags'

Error details: {info}"""
    
    # Check if the model is available
    available_models = info
    if not any(model_name in model for model in available_models):
        return f"""Model '{model_name}' not found.

Available models: {', '.join(available_models) if available_models else 'None'}

To install CodeLlama:
- ollama pull codellama
- ollama pull codellama:7b
- ollama pull codellama:13b
- ollama pull codellama:34b"""
    
    # Craft a specific prompt for zsh alias/function generation
    system_prompt = f"""You are an expert in zsh shell scripting. Based on the user's request, generate either a zsh alias or function named '{alias_name}'.

Rules:
1. If the task is simple (single command or command with basic options), create an alias: alias {alias_name}='command here'
2. If the task requires parameters, loops, conditionals, or multiple commands, create a function:
   {alias_name}() {{
       # function body here
   }}
3. For functions, include parameter handling with $1, $2, etc. if needed
4. Only return the alias or function definition, no explanations or markdown formatting
5. Make the code efficient and follow zsh best practices
6. If parameters are needed, make them intuitive and well-handled

Task: {prompt}
Generate a zsh alias or function named '{alias_name}'"""
    
    full_prompt = system_prompt
    
    # Prepare the request payload
    payload = {
        "model": model_name,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,  # Low temperature for more deterministic code
            "top_p": 0.9,
            "num_predict": 500
        }
    }
    
    try:
        # Make request to Ollama API
        response = requests.post(
            f"{model_url}/api/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
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
        return f"Error connecting to Ollama: {e}\n\nTroubleshooting:\n- Ensure Ollama is running: 'ollama serve'\n- Check the URL: {model_url}"
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
  python codellama_zsh.py findpy "find all .py files modified in the last 7 days"
  python codellama_zsh.py backup "create a backup of my home directory excluding hidden files"  
  python codellama_zsh.py gitlog "show git log with pretty formatting"
  python codellama_zsh.py --interactive
        """
    )
    
    parser.add_argument(
        "alias_name",
        help="Name for the alias or function"
    )
    
    parser.add_argument(
        "prompt",
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
    
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check Ollama status and available models"
    )
    
    args = parser.parse_args()
    
    if args.check:
        print("Checking Ollama status...")
        is_running, info = check_ollama_status(args.model_url)
        if is_running:
            print(f"✓ Ollama is running at {args.model_url}")
            print(f"Available models: {', '.join(info) if info else 'None'}")
        else:
            print(f"✗ Ollama is not accessible at {args.model_url}")
            print(f"Error: {info}")
            print("\nTo start Ollama:")
            print("1. Run: ollama serve")
            print("2. Or just: ollama (on some systems)")
        return
    
    if args.interactive:
        print("CodeLlama ZSH Alias/Function Generator (Interactive Mode)")
        print("Format: <alias_name> <description>")
        print("Type 'quit' or 'exit' to stop\n")
        
        while True:
            try:
                user_input = input("zsh> ").strip()
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                if not user_input:
                    continue
                
                # Parse alias name and prompt from input
                parts = user_input.split(' ', 1)
                if len(parts) < 2:
                    print("Please provide both alias name and description: <alias_name> <description>")
                    continue
                
                alias_name, prompt = parts
                print(f"Generating zsh alias/function '{alias_name}'...")
                result = generate_zsh_code(alias_name, prompt, args.model_url, args.model)
                print(f"\n{result}\n")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
                
    elif args.alias_name and args.prompt:
        print(f"Generating zsh alias/function '{args.alias_name}'...")
        result = generate_zsh_code(args.alias_name, args.prompt, args.model_url, args.model)
        print(result)
        
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()