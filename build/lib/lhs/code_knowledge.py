from lhs.llm import embed, prompt, LLMOpts
import lhs.paths as paths
import lhs.system_prompts as system_prompts
import os
import numpy
import json

def get_file_from_prompt(prompt_text: str):
  prompt_embedding = embed(prompt_text)

  # Get all metadata files
  metadata_files = []
  codebase_metadata_dir = paths.get_codebase_metadata_dir()
  
  for root, dirs, files in os.walk(codebase_metadata_dir):
    for file in files:
      if file.endswith('.json'):
        metadata_files.append(os.path.join(root, file))
  
  # Calculate cosine similarity between prompt embedding and each metadata file embedding
  similarities = []
  for metadata_file in metadata_files:
    # Get the corresponding .npy file path
    embedding_file = metadata_file.replace('.json', '.npy')
    
    if os.path.exists(embedding_file):
      try:
        # Load the embedding from .npy file
        metadata_embedding = numpy.load(embedding_file)
        
        # Calculate cosine similarity
        similarity = numpy.dot(prompt_embedding, metadata_embedding) / (
          numpy.linalg.norm(prompt_embedding) * numpy.linalg.norm(metadata_embedding)
        )
        
        similarities.append((metadata_file, similarity))
        
      except Exception as e:
        print(f"Error processing {embedding_file}: {e}")
    else:
      print(f"Embedding file not found: {embedding_file}")
  
  # Sort by similarity (highest first)
  similarities.sort(key=lambda x: x[1], reverse=True)
  
  # Get the most similar file
  if similarities:
    most_similar_file = similarities[0][0]
    return most_similar_file
  else:
    return None
  
def get_example_call(prompt_text: str):
  file = get_file_from_prompt(prompt_text)

  with open(file, 'r') as f:
    code = f.read()

  example_call = prompt(system_prompts.EXAMPLE_CALL, f"File name:{file}\nCode:{code}", LLMOpts())
  print(example_call)
  return example_call

  