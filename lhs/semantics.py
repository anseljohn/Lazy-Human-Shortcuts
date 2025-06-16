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