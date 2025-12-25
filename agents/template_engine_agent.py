"""
TemplateEngineAgent
===================
Agent 4: Define and apply content templates.

Responsibility:
- Load template definitions from JSON files
- Map template fields to content logic blocks
- Render templates with product data
- Validate rendered output

Input: Template definitions + data from logic blocks
Output: Rendered content structures
LLM Usage: No (template rendering only)
"""

import json
from typing import Dict, Any, List, Optional
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import TEMPLATES_DIR


class TemplateEngineAgent:
    """
    Agent responsible for loading and applying templates.
    
    Templates define the structure of output pages and map
    fields to content logic blocks. This agent handles
    template rendering without LLM calls.
    """
    
    def __init__(self):
        """Initialize the TemplateEngineAgent."""
        self.name = "TemplateEngineAgent"
        self.templates_dir = TEMPLATES_DIR
        self.templates: Dict[str, Dict] = {}
        
        # Load all templates on initialization
        self._load_templates()
    
    def _load_templates(self) -> None:
        """Load all template definitions from templates directory."""
        template_files = {
            "faq": "faq_template.json",
            "product": "product_template.json",
            "comparison": "comparison_template.json"
        }
        
        for name, filename in template_files.items():
            filepath = self.templates_dir / filename
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.templates[name] = json.load(f)
            else:
                # Use default template if file doesn't exist
                self.templates[name] = self._get_default_template(name)
    
    def _get_default_template(self, template_name: str) -> Dict[str, Any]:
        """Get default template definition."""
        defaults = {
            "faq": {
                "template_name": "faq",
                "description": "FAQ page template",
                "fields": {
                    "page_type": {"type": "string", "default": "faq"},
                    "product_name": {"type": "string", "source": "product.name"},
                    "generated_at": {"type": "datetime", "source": "system.timestamp"},
                    "faqs": {
                        "type": "array",
                        "item_fields": {
                            "question": {"type": "string"},
                            "answer": {"type": "string"},
                            "category": {"type": "string"}
                        }
                    }
                },
                "required_blocks": ["safety", "usage", "benefits", "ingredients"]
            },
            "product": {
                "template_name": "product",
                "description": "Product page template",
                "fields": {
                    "page_type": {"type": "string", "default": "product"},
                    "product_name": {"type": "string", "source": "product.name"},
                    "ingredients": {"type": "array", "source": "blocks.ingredients"},
                    "benefits": {"type": "array", "source": "blocks.benefits"},
                    "usage": {"type": "string", "source": "blocks.usage"},
                    "side_effects": {"type": "string", "source": "blocks.safety"},
                    "price": {"type": "string", "source": "product.price"}
                },
                "required_blocks": ["ingredients", "benefits", "usage", "safety"]
            },
            "comparison": {
                "template_name": "comparison",
                "description": "Comparison page template",
                "fields": {
                    "page_type": {"type": "string", "default": "comparison"},
                    "product_a": {"type": "object", "source": "product_a"},
                    "product_b": {"type": "object", "source": "product_b"},
                    "comparison": {
                        "type": "object",
                        "fields": {
                            "ingredients": {"type": "string"},
                            "benefits": {"type": "string"},
                            "price": {"type": "string"}
                        },
                        "source": "blocks.comparison"
                    }
                },
                "required_blocks": ["comparison"]
            }
        }
        return defaults.get(template_name, {})
    
    def get_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a template definition by name.
        
        Args:
            template_name: Name of the template (faq, product, comparison)
            
        Returns:
            Template definition dictionary or None
        """
        return self.templates.get(template_name)
    
    def get_required_blocks(self, template_name: str) -> List[str]:
        """
        Get list of required logic blocks for a template.
        
        Args:
            template_name: Name of the template
            
        Returns:
            List of required block names
        """
        template = self.get_template(template_name)
        if template:
            return template.get("required_blocks", [])
        return []
    
    def list_templates(self) -> List[str]:
        """Return list of available template names."""
        return list(self.templates.keys())
    
    def validate_template_data(
        self, 
        template_name: str, 
        data: Dict[str, Any]
    ) -> bool:
        """
        Validate that data matches template requirements.
        
        Args:
            template_name: Name of the template
            data: Data to validate
            
        Returns:
            True if valid, raises ValueError otherwise
        """
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template not found: {template_name}")
        
        required_fields = template.get("fields", {})
        
        for field_name, field_def in required_fields.items():
            if field_def.get("required", True) and field_name not in data:
                if "default" not in field_def:
                    raise ValueError(f"Missing required field: {field_name}")
        
        return True
    
    def render_faq_item(
        self, 
        question: str, 
        answer: str, 
        category: str
    ) -> Dict[str, str]:
        """
        Render a single FAQ item using the template.
        
        Args:
            question: The question text
            answer: The answer text
            category: Question category
            
        Returns:
            Structured FAQ item
        """
        return {
            "question": question,
            "answer": answer,
            "category": category
        }
    
    def get_template_schema(self, template_name: str) -> Dict[str, Any]:
        """
        Get the JSON schema for a template's output.
        
        Args:
            template_name: Name of the template
            
        Returns:
            JSON schema dictionary
        """
        template = self.get_template(template_name)
        if not template:
            return {}
        
        return {
            "type": "object",
            "properties": {
                field: {"type": props.get("type", "string")}
                for field, props in template.get("fields", {}).items()
            }
        }
    
    def __repr__(self) -> str:
        return f"<{self.name} templates={self.list_templates()}>"


# =============================================================================
# STANDALONE EXECUTION (for testing)
# =============================================================================

if __name__ == "__main__":
    agent = TemplateEngineAgent()
    
    print("TemplateEngineAgent Test")
    print("=" * 50)
    
    print(f"\nAvailable templates: {agent.list_templates()}")
    
    for template_name in agent.list_templates():
        print(f"\n--- {template_name.upper()} Template ---")
        template = agent.get_template(template_name)
        print(json.dumps(template, indent=2))
        print(f"Required blocks: {agent.get_required_blocks(template_name)}")
