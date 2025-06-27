# 100% AI
from dataclasses import dataclass
from openai import OpenAI
from anthropic import Anthropic
from typing import Optional
from enum import Enum

import lhs.vars as vars

import os

class LLMType(Enum):
  SIMPLE = "simple"
  MID = "mid"
  COMPLEX = "complex"
  EMBEDDING = "embedding"

@dataclass
class LLMOpts:
  temperature: float = 0.2
  max_tokens: int = 600
  top_p: float = 1.0
  presence_penalty: float = 0.0
  frequency_penalty: float = 0.0
  seed: Optional[int] = vars.seed
  complexity: LLMType = LLMType.MID

def _get_model(complexity: LLMType) -> tuple[str, str]:
  if complexity == LLMType.SIMPLE:
    return "claude-3-5-haiku-20241022", "anthropic"
  elif complexity == LLMType.MID:
    return "claude-sonnet-4-20250514", "anthropic"
  elif complexity == LLMType.COMPLEX:
    return "gpt-4o", "openai"
  elif complexity == LLMType.EMBEDDING:
    return "text-embedding-3-small", "openai"
  else:
    return "claude-3-5-haiku-20241022", "anthropic"  # default to simple

def prompt(sys_prompt: str, usr_prompt: str, opts: LLMOpts) -> str:
  model, provider = _get_model(opts.complexity)
  
  if provider == "openai":
    client = OpenAI(api_key=os.getenv("LHS_OPENAI_KEY"))
    response = client.chat.completions.create(
      model=model,
      messages=[
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": usr_prompt}
      ],
      temperature=opts.temperature,
      top_p=opts.top_p,
      presence_penalty=opts.presence_penalty,
      frequency_penalty=opts.frequency_penalty,
      max_tokens=opts.max_tokens,
      seed=opts.seed
    )
    return response.choices[0].message.content.strip()
  
  elif provider == "anthropic":
    client = Anthropic(api_key=os.getenv("LHS_ANTHROPIC_KEY"))
    response = client.messages.create(
      model=model,
      max_tokens=opts.max_tokens,
      temperature=opts.temperature,
      system=sys_prompt,
      messages=[{"role": "user", "content": usr_prompt}]
    )
    return response.content[0].text.strip()

def embed(text: str) -> list[float]:
  client = OpenAI(api_key=os.getenv("LHS_OPENAI_KEY"))
  response = client.embeddings.create(
    model="text-embedding-3-small",
    input=text,
    encoding_format="float"
  )
  return response.data[0].embedding