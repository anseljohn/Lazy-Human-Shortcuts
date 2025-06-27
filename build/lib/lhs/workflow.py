from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from enum import Enum
import json
import hashlib
from datetime import datetime
import numpy as np
import re
from pathlib import Path

import lhs.paths as paths
from lhs.llm import embed, prompt, LLMOpts

class WorkflowStepType(Enum):
    QUERY_ANALYSIS = "query_analysis"
    COMPLEXITY_DETERMINATION = "complexity_determination"
    SCRIPT_GENERATION = "script_generation"
    SCRIPT_EXECUTION = "script_execution"
    OUTPUT_FORMATTING = "output_formatting"
    ERROR_HANDLING = "error_handling"

@dataclass
class WorkflowStep:
    step_type: WorkflowStepType
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    execution_time_ms: float
    success: bool
    error_message: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        data = asdict(self)
        data['step_type'] = self.step_type.value
        return data
    
    @classmethod
    def from_dict(cls, data):
        data['step_type'] = WorkflowStepType(data['step_type'])
        return cls(**data)

@dataclass
class ScriptTemplate:
    """A reusable script template that can be adapted for similar queries."""
    id: str
    original_query: str
    query_embedding: List[float]
    script_template: str
    complexity: str
    success_count: int = 0
    total_usage: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_used: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        data = asdict(self)
        return data
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class ScriptAdapter:
    """Adapts script templates to new queries."""
    
    @staticmethod
    def adapt_script(template: ScriptTemplate, new_query: str) -> str:
        """Adapt a script template to a new query."""
        # Simple adaptation rules
        adapted_script = template.script_template
        
        # Rule 1: Handle repetition patterns
        if "times" in new_query.lower() or "repeat" in new_query.lower():
            # Extract number from query
            numbers = re.findall(r'\d+', new_query)
            if numbers:
                count = int(numbers[0])
                # If it's a simple echo command, make it repeat
                if "echo" in adapted_script:
                    adapted_script = f"for i in {{1..{count}}}; do {adapted_script}; done"
        
        # Rule 2: Handle file/directory changes
        if "current directory" in template.original_query.lower() and "different directory" in new_query.lower():
            # Extract directory from new query
            dir_match = re.search(r'in\s+([^\s]+)', new_query)
            if dir_match:
                directory = dir_match.group(1)
                adapted_script = adapted_script.replace("ls", f"ls {directory}")
        
        # Rule 3: Handle output format changes
        if "json" in new_query.lower() and "json" not in template.original_query.lower():
            if "ls" in adapted_script:
                adapted_script = adapted_script.replace("ls", "ls -la | jq -R -s 'split(\"\\n\")[:-1] | map({file: .})'")
        
        # Rule 4: Handle verbosity changes
        if "verbose" in new_query.lower() or "detailed" in new_query.lower():
            if "ls" in adapted_script and "-la" not in adapted_script:
                adapted_script = adapted_script.replace("ls", "ls -la")
        
        return adapted_script

class WorkflowManager:
    def __init__(self):
        self.templates_file = paths.get_script_templates_file()
        self.templates: Dict[str, ScriptTemplate] = {}
        self.load_templates()
    
    def load_templates(self):
        """Load existing script templates from file."""
        if Path(self.templates_file).exists():
            try:
                with open(self.templates_file, 'r') as f:
                    templates_data = json.load(f)
                    for template_id, template_data in templates_data.items():
                        self.templates[template_id] = ScriptTemplate.from_dict(template_data)
            except Exception as e:
                print(f"Error loading templates: {e}")
    
    def save_templates(self):
        """Save script templates to file."""
        templates_data = {tid: template.to_dict() for tid, template in self.templates.items()}
        with open(self.templates_file, 'w') as f:
            json.dump(templates_data, f, indent=2)
    
    def create_template_id(self, query: str) -> str:
        """Create a unique ID for a template based on query."""
        return hashlib.md5(query.encode()).hexdigest()[:16]
    
    def find_similar_template(self, query: str, similarity_threshold: float = 0.75) -> Optional[ScriptTemplate]:
        """Find a similar script template based on query embedding similarity."""
        if not self.templates:
            return None
        
        query_embedding = embed(query)
        best_match = None
        best_similarity = 0.0
        
        for template in self.templates.values():
            similarity = self.calculate_cosine_similarity(query_embedding, template.query_embedding)
            if similarity > best_similarity and similarity >= similarity_threshold:
                best_similarity = similarity
                best_match = template
        
        return best_match
    
    def calculate_cosine_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings."""
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def create_template(self, query: str, script: str, complexity: str) -> ScriptTemplate:
        """Create a new script template."""
        template_id = self.create_template_id(query)
        query_embedding = embed(query)
        
        template = ScriptTemplate(
            id=template_id,
            original_query=query,
            query_embedding=query_embedding,
            script_template=script,
            complexity=complexity
        )
        
        self.templates[template_id] = template
        return template
    
    def update_template_usage(self, template: ScriptTemplate, success: bool = True):
        """Update template usage statistics."""
        template.total_usage += 1
        template.last_used = datetime.now().isoformat()
        if success:
            template.success_count += 1
    
    def get_or_create_script(self, query: str, complexity: str) -> tuple[str, bool]:
        """
        Get an adapted script from existing template or create new one.
        Returns (script, was_cached)
        """
        # Try to find similar template
        similar_template = self.find_similar_template(query)
        
        if similar_template:
            # Adapt existing template
            adapted_script = ScriptAdapter.adapt_script(similar_template, query)
            self.update_template_usage(similar_template)
            return adapted_script, True
        else:
            # Generate new script
            script = prompt(system_prompts.BASH_PROMPT, query, LLMOpts(complexity=complexity))
            template = self.create_template(query, script, complexity)
            return script, False
    
    def get_template_statistics(self) -> Dict[str, Any]:
        """Get statistics about all templates."""
        if not self.templates:
            return {"total_templates": 0}
        
        total_templates = len(self.templates)
        total_usage = sum(t.total_usage for t in self.templates.values())
        total_success = sum(t.success_count for t in self.templates.values())
        success_rate = total_success / total_usage if total_usage > 0 else 0
        
        complexity_distribution = {}
        for template in self.templates.values():
            complexity_distribution[template.complexity] = complexity_distribution.get(template.complexity, 0) + 1
        
        return {
            "total_templates": total_templates,
            "total_usage": total_usage,
            "success_rate": success_rate,
            "complexity_distribution": complexity_distribution
        }

# Global workflow manager instance
_workflow_manager = None

def get_workflow_manager() -> WorkflowManager:
    """Get the global workflow manager instance."""
    global _workflow_manager
    if _workflow_manager is None:
        _workflow_manager = WorkflowManager()
    return _workflow_manager

def create_workflow_step(step_type: WorkflowStepType, input_data: Dict[str, Any], 
                        output_data: Dict[str, Any], execution_time_ms: float, 
                        success: bool, error_message: Optional[str] = None) -> WorkflowStep:
    """Create a workflow step."""
    return WorkflowStep(
        step_type=step_type,
        input_data=input_data,
        output_data=output_data,
        execution_time_ms=execution_time_ms,
        success=success,
        error_message=error_message
    ) 