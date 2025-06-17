import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("LHS_OPENAI_KEY"))

def describe_command(alias_name, command):
    prompt = f"""
You are an assistant that writes clear, concise descriptions of shell aliases for developers.

Return:
- A short sentence (5–12 words) if the command is simple.
- A longer sentence or two if the command is complex or multi-step.

Examples:
Alias: deploy
Command: git push origin main
Description: Pushes to the main branch.

Alias: build
Command: bazel build //... && ./scripts/post.sh
Description: Builds the Bazel project and runs post-build tasks.

Here is the alias you need to describe:
Alias: {alias_name}
Command: {command}
Description:"""

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=100,
    )

    text = response.choices[0].message.content.strip()
    # Just in case, take the first line or two words
    return " ".join(text.split())

def describe_tool(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    prompt = f"""
You are an intelligent code analysis assistant.

Analyze the following Python script and do the following:
1. Describe in 1–2 sentences what the script does.
2. Determine if and how it can be run from the command line.
3. If it uses argparse or click, list the available flags and what they do.
4. If possible, show a sample command to run it.

Python script:
{code}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=600,
    )

    return response.choices[0].message.content.strip()

# Example usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python smart_usage.py <file.py>")
        exit(1)

    print(describe_tool(sys.argv[1]))
