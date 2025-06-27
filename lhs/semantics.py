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
Create a concise and accurate description of a given piece of code, focusing on its functionality, purpose, and key components. Avoid detailing unnecessary implementation specifics unless they are crucial for understanding the main function.

# Steps

1. **Analyze the Code**: Review the logic, data structures, and overall flow to understand the main function and any supporting details crucial for its operation.
2. **Identify Key Components**: Note main variables, functions, or classes that play a key role in the code's operation.
3. **Determine Purpose and Functionality**: Consider what the overall intent of the code is and how it achieves it through the identified components.
4. **Construct Description**: Formulate a brief paragraph describing the purpose and core functionality, highlighting the key components and their role.

# Output Format

A short paragraph detailing the code's functionality and purpose, between 1 and 2 sentences long.

# Examples

**Input**: A function that calculates the factorial of a number using recursion.

**Output**: The code defines a recursive function to calculate the factorial of a given non-negative integer.

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
