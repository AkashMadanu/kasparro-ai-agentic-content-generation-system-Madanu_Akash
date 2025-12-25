"""
ProductPageAgent
================
Agent 6: Generate product description page.

Responsibility:
- Use parsed product data
- Apply ContentLogicAgent blocks
- Apply Product template
- Output structured product_page.json

Input: Parsed product data
Output: product_page.json structure
LLM Usage: Yes (for enhanced descriptions)
"""

import json
from datetime import datetime, timezone
from typing import Dict, Any
from pathlib import Path

import google.generativeai as genai

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import GEMINI_API_KEY, GEMINI_MODEL, LLM_CONFIG


class ProductPageAgent:
    """
    Agent responsible for generating the product description page.
    
    This agent takes parsed product data and generates a comprehensive
    product page with enhanced descriptions using LLM.
    """
    
    def __init__(self):
        """Initialize the ProductPageAgent with Gemini."""
        self.name = "ProductPageAgent"
        
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config=genai.GenerationConfig(
                temperature=LLM_CONFIG["temperature"],
                top_p=LLM_CONFIG["top_p"],
                top_k=LLM_CONFIG["top_k"],
                max_output_tokens=LLM_CONFIG["max_output_tokens"],
                response_mime_type="application/json"
            )
        )
    
    def generate(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate the product page.
        
        Args:
            product: Parsed product object
            
        Returns:
            Structured product page JSON
        """
        # Generate enhanced content using LLM
        enhanced_content = self._generate_enhanced_content(product)
        
        # Build final product page structure
        product_page = {
            "page_type": "product",
            "product_id": product.get("id", ""),
            "product_name": product.get("name", ""),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            
            # Core product information
            "headline": enhanced_content.get("headline", product.get("name", "")),
            "description": enhanced_content.get("description", ""),
            
            # Structured data
            "concentration": f"{product.get('concentration', '')}%",
            "skin_type": product.get("skin_type", []),
            "ingredients": {
                "list": product.get("ingredients", []),
                "description": enhanced_content.get("ingredients_description", "")
            },
            "benefits": {
                "list": product.get("benefits", []),
                "description": enhanced_content.get("benefits_description", "")
            },
            "usage": {
                "instructions": product.get("usage", ""),
                "tips": enhanced_content.get("usage_tips", [])
            },
            "safety": {
                "side_effects": product.get("side_effects", ""),
                "precautions": enhanced_content.get("precautions", [])
            },
            "pricing": {
                "amount": product.get("price", 0),
                "currency": "INR",
                "formatted": f"₹{product.get('price', '')}"
            }
        }
        
        return product_page
    
    def _generate_enhanced_content(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Generate enhanced descriptions using LLM."""
        prompt = self._build_prompt(product)
        response = self._call_llm(prompt)
        return self._parse_response(response)
    
    def _build_prompt(self, product: Dict[str, Any]) -> str:
        """Build prompt for content enhancement."""
        return f"""You are the ProductPageAgent in a multi-agent content generation system.

Your task is to generate enhanced product page content for a skincare product.

PRODUCT DATA:
- Name: {product.get('name', '')}
- Concentration: {product.get('concentration', '')}%
- Skin Types: {', '.join(product.get('skin_type', []))}
- Key Ingredients: {', '.join(product.get('ingredients', []))}
- Benefits: {', '.join(product.get('benefits', []))}
- How to Use: {product.get('usage', '')}
- Side Effects: {product.get('side_effects', '')}
- Price: ₹{product.get('price', '')}

REQUIREMENTS:
1. Generate content based ONLY on the provided product data
2. Do NOT make up new facts or features
3. Keep descriptions professional and engaging
4. All content must be accurate to the input data

OUTPUT FORMAT (strict JSON):
{{
    "headline": "A catchy product headline",
    "description": "A 2-3 sentence product description",
    "ingredients_description": "Brief explanation of the key ingredients",
    "benefits_description": "Brief explanation of the benefits",
    "usage_tips": ["tip 1", "tip 2"],
    "precautions": ["precaution 1", "precaution 2"]
}}

Generate the content now. Return ONLY valid JSON, no explanations."""
    
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
            # Return minimal structure if parsing fails
            return {
                "headline": "",
                "description": "",
                "ingredients_description": "",
                "benefits_description": "",
                "usage_tips": [],
                "precautions": []
            }
    
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
    
    agent = ProductPageAgent()
    result = agent.generate(sample_product)
    
    print("ProductPageAgent Test")
    print("=" * 50)
    print(json.dumps(result, indent=2))
