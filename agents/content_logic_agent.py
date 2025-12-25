"""
ContentLogicAgent
=================
Agent 3: Expose reusable content logic blocks.

Responsibility:
- Provide pure functions for content transformation
- Generate structured JSON fragments
- Act as a facade for all logic block operations

Input: Product data
Output: Structured JSON fragments
LLM Usage: Yes (for complex transformations)

This agent wraps the logic_blocks modules and provides a unified interface.
"""

import json
from typing import Dict, Any, List
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))
from logic_blocks import (
    generate_benefits,
    generate_usage,
    generate_safety,
    generate_ingredients,
    compare_products
)


class ContentLogicAgent:
    """
    Agent that exposes reusable content logic blocks.
    
    This agent acts as a facade for the logic_blocks module,
    providing a unified interface for content transformation.
    Each method returns a structured JSON fragment.
    """
    
    def __init__(self):
        """Initialize the ContentLogicAgent."""
        self.name = "ContentLogicAgent"
        self.available_blocks = [
            "generateBenefits",
            "generateUsage", 
            "generateSafety",
            "generateIngredients",
            "compareProducts"
        ]
    
    def generate_benefits(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate benefits content block.
        
        Args:
            product: Parsed product object
            
        Returns:
            Structured benefits fragment
        """
        return generate_benefits(product)
    
    def generate_usage(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate usage content block.
        
        Args:
            product: Parsed product object
            
        Returns:
            Structured usage fragment
        """
        return generate_usage(product)
    
    def generate_safety(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate safety content block.
        
        Args:
            product: Parsed product object
            
        Returns:
            Structured safety fragment
        """
        return generate_safety(product)
    
    def generate_ingredients(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate ingredients content block.
        
        Args:
            product: Parsed product object
            
        Returns:
            Structured ingredients fragment
        """
        return generate_ingredients(product)
    
    def compare_products(
        self, 
        product_a: Dict[str, Any], 
        product_b: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compare two products and generate comparison content.
        
        Args:
            product_a: First product object
            product_b: Second product object
            
        Returns:
            Structured comparison fragment
        """
        return compare_products(product_a, product_b)
    
    def get_all_blocks(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate all content blocks for a product.
        
        Args:
            product: Parsed product object
            
        Returns:
            Dictionary containing all content blocks
        """
        return {
            "benefits": self.generate_benefits(product),
            "usage": self.generate_usage(product),
            "safety": self.generate_safety(product),
            "ingredients": self.generate_ingredients(product)
        }
    
    def list_available_blocks(self) -> List[str]:
        """Return list of available logic blocks."""
        return self.available_blocks.copy()
    
    def __repr__(self) -> str:
        return f"<{self.name} blocks={self.available_blocks}>"


# =============================================================================
# STANDALONE EXECUTION (for testing)
# =============================================================================

if __name__ == "__main__":
    # Test with sample product
    sample_product = {
        "id": "glowboost-vitamin-c-serum-abc123",
        "name": "GlowBoost Vitamin C Serum",
        "concentration": 10.0,
        "skin_type": ["Oily", "Combination"],
        "ingredients": ["Vitamin C", "Hyaluronic Acid"],
        "benefits": ["Brightening", "Fades dark spots"],
        "usage": "Apply 2–3 drops in the morning before sunscreen",
        "side_effects": "Mild tingling for sensitive skin",
        "price": 699.0
    }
    
    agent = ContentLogicAgent()
    
    print("ContentLogicAgent Test")
    print("=" * 50)
    
    print("\n1. Benefits Block:")
    print(json.dumps(agent.generate_benefits(sample_product), indent=2))
    
    print("\n2. Usage Block:")
    print(json.dumps(agent.generate_usage(sample_product), indent=2))
    
    print("\n3. Safety Block:")
    print(json.dumps(agent.generate_safety(sample_product), indent=2))
    
    print("\n4. Ingredients Block:")
    print(json.dumps(agent.generate_ingredients(sample_product), indent=2))
    
    print(f"\nAvailable blocks: {agent.list_available_blocks()}")
