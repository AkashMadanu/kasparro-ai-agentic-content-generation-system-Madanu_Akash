"""
ComparisonAgent
===============
Agent 7: Create fictional Product B and comparison page.

Responsibility:
- Generate a fictional competitor product (Product B)
- Compare Product A vs Product B
- Output structured comparison_page.json

Input: Product A data
Output: comparison_page.json structure
LLM Usage: Yes (for Product B creation and comparison)
"""

import json
from datetime import datetime, timezone
from typing import Dict, Any
from pathlib import Path

import google.generativeai as genai

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import GEMINI_API_KEY, GEMINI_MODEL, LLM_CONFIG


class ComparisonAgent:
    """
    Agent responsible for generating the comparison page.
    
    This agent creates a fictional competitor product and
    generates a detailed comparison between the two products.
    """
    
    def __init__(self):
        """Initialize the ComparisonAgent with Gemini."""
        self.name = "ComparisonAgent"
        
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config=genai.GenerationConfig(
                temperature=0.5,  # Slightly higher for creativity
                top_p=LLM_CONFIG["top_p"],
                top_k=LLM_CONFIG["top_k"],
                max_output_tokens=LLM_CONFIG["max_output_tokens"],
                response_mime_type="application/json"
            )
        )
    
    def generate(self, product_a: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate the comparison page.
        
        Args:
            product_a: Parsed product object (the main product)
            
        Returns:
            Structured comparison page JSON
        """
        # Generate fictional Product B
        product_b = self._generate_product_b(product_a)
        
        # Generate comparison analysis
        comparison = self._generate_comparison(product_a, product_b)
        
        # Build final comparison page structure
        comparison_page = {
            "page_type": "comparison",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "product_a": {
                "id": product_a.get("id", ""),
                "name": product_a.get("name", ""),
                "concentration": f"{product_a.get('concentration', '')}%",
                "ingredients": product_a.get("ingredients", []),
                "benefits": product_a.get("benefits", []),
                "skin_type": product_a.get("skin_type", []),
                "price": f"₹{product_a.get('price', '')}"
            },
            "product_b": product_b,
            "comparison": comparison,
            "recommendation": self._generate_recommendation(product_a, product_b, comparison)
        }
        
        return comparison_page
    
    def _generate_product_b(self, product_a: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a fictional competitor product."""
        prompt = f"""You are the ComparisonAgent in a multi-agent content generation system.

Your task is to create a FICTIONAL competitor skincare product to compare against.

PRODUCT A (Real Product):
- Name: {product_a.get('name', '')}
- Concentration: {product_a.get('concentration', '')}%
- Skin Types: {', '.join(product_a.get('skin_type', []))}
- Key Ingredients: {', '.join(product_a.get('ingredients', []))}
- Benefits: {', '.join(product_a.get('benefits', []))}
- Price: ₹{product_a.get('price', '')}

REQUIREMENTS:
1. Create a FICTIONAL product that is similar but different
2. The product should be a reasonable competitor (similar category)
3. Use different but plausible ingredients
4. Price should be in a similar range (can be higher or lower)
5. Give it a creative but believable name
6. This is FICTIONAL - do not use any real product names

OUTPUT FORMAT (strict JSON):
{{
    "id": "fictional-product-id",
    "name": "Fictional Product Name",
    "concentration": "XX%",
    "ingredients": ["ingredient1", "ingredient2"],
    "benefits": ["benefit1", "benefit2"],
    "skin_type": ["type1", "type2"],
    "price": "₹XXX",
    "is_fictional": true
}}

Generate the fictional product now. Return ONLY valid JSON, no explanations."""
        
        response = self._call_llm(prompt)
        return self._parse_response(response)
    
    def _generate_comparison(
        self, 
        product_a: Dict[str, Any], 
        product_b: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate comparison analysis between two products."""
        prompt = f"""You are the ComparisonAgent in a multi-agent content generation system.

Your task is to compare two skincare products.

PRODUCT A:
- Name: {product_a.get('name', '')}
- Concentration: {product_a.get('concentration', '')}%
- Ingredients: {', '.join(product_a.get('ingredients', []))}
- Benefits: {', '.join(product_a.get('benefits', []))}
- Price: ₹{product_a.get('price', '')}

PRODUCT B:
- Name: {product_b.get('name', '')}
- Concentration: {product_b.get('concentration', '')}
- Ingredients: {', '.join(product_b.get('ingredients', []))}
- Benefits: {', '.join(product_b.get('benefits', []))}
- Price: {product_b.get('price', '')}

REQUIREMENTS:
1. Compare ingredients - what's different, what's similar
2. Compare benefits - which has better/different benefits
3. Compare price - value proposition
4. Be objective and factual based on the data provided
5. Keep each comparison to 2-3 sentences

OUTPUT FORMAT (strict JSON):
{{
    "ingredients": "Comparison of ingredients...",
    "benefits": "Comparison of benefits...",
    "price": "Comparison of price and value...",
    "skin_type": "Comparison of target skin types...",
    "overall": "Overall comparison summary..."
}}

Generate the comparison now. Return ONLY valid JSON, no explanations."""
        
        response = self._call_llm(prompt)
        return self._parse_response(response)
    
    def _generate_recommendation(
        self,
        product_a: Dict[str, Any],
        product_b: Dict[str, Any],
        comparison: Dict[str, str]
    ) -> Dict[str, Any]:
        """Generate recommendation based on comparison."""
        return {
            "best_for_value": product_a.get("name", "") if product_a.get("price", 0) <= float(str(product_b.get("price", "0")).replace("₹", "").replace(",", "") or 0) else product_b.get("name", ""),
            "note": "Recommendation based on provided product data. Individual results may vary based on skin type and preferences.",
            "disclaimer": "Product B is fictional and created for comparison purposes only."
        }
    
    def _call_llm(self, prompt: str) -> str:
        """Call Gemini API."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"LLM call failed: {str(e)}")
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response."""
        try:
            cleaned = response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            return json.loads(cleaned.strip())
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response: {str(e)}")
    
    def __repr__(self) -> str:
        return f"<{self.name}>"


# =============================================================================
# STANDALONE EXECUTION (for testing)
# =============================================================================

if __name__ == "__main__":
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
    
    agent = ComparisonAgent()
    result = agent.generate(sample_product)
    
    print("ComparisonAgent Test")
    print("=" * 50)
    print(json.dumps(result, indent=2))
