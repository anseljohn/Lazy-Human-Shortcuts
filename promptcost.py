import os
import tiktoken

# --- CONFIG ---
MODEL = "gpt-4o"
INPUT_COST_PER_1K = 0.005  # USD
# ---------------

def get_all_text_from_dir(directory, include_ext={'.py', '.txt', '.md', '.json', '.yaml', '.yml', '.sh', '.js', '.cpp', '.h'}):
    all_text = []
    for root, _, files in os.walk(directory):
        for f in files:
            path = os.path.join(root, f)
            ext = os.path.splitext(f)[1].lower()
            if ext in include_ext:
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        all_text.append(f"# File: {path}\n{content}\n\n")
                except Exception as e:
                    print(f"Skipped {path} (error: {e})")
    return "".join(all_text)

def count_tokens(text, model=MODEL):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

def estimate_cost(prompt_tokens, cost_per_1k=INPUT_COST_PER_1K):
    return round(prompt_tokens / 1000 * cost_per_1k, 6)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python estimate_gpt4o_cost.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    print(f"Scanning directory: {directory}")

    content = get_all_text_from_dir(directory)
    token_count = count_tokens(content)
    cost = estimate_cost(token_count)

    print("\n--- GPT-4o Prompt Cost Estimate ---")
    print(f"Total tokens: {token_count}")
    print(f"Estimated cost (input only): ${cost}")
