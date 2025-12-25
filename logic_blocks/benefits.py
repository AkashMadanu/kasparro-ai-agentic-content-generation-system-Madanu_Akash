"""
Benefits Logic Block
====================
Pure function to generate benefits content from product data.
"""

from typing import Dict, Any, List


def generate_benefits(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate benefits content block from product data.
    
    This is a pure function that transforms product benefits data
    into a structured content fragment.
    
    Args:
        product: Parsed product object containing 'benefits' field
        
    Returns:
        Structured benefits content fragment
        
    Example Output:
        {
            "type": "benefits",
            "title": "Key Benefits",
            "items": [
                {"benefit": "Brightening", "description": "..."},
                ...
            ],
            "summary": "..."
        }
    """
    benefits_list = product.get("benefits", [])
    product_name = product.get("name", "This product")
    ingredients = product.get("ingredients", [])
    
    # Build structured benefits items
    items = []
    for benefit in benefits_list:
        items.append({
            "benefit": benefit,
            "description": _generate_benefit_description(benefit, ingredients)
        })
    
    # Generate summary
    summary = _generate_benefits_summary(product_name, benefits_list)
    
    return {
        "type": "benefits",
        "title": "Key Benefits",
        "count": len(items),
        "items": items,
        "summary": summary,
        "product_name": product_name
    }


def _generate_benefit_description(benefit: str, ingredients: List[str]) -> str:
    """
    Generate a description for a specific benefit.
    
    Uses rule-based logic to create descriptions based on
    the benefit name and available ingredients.
    """
    benefit_lower = benefit.lower()
    ingredient_str = ", ".join(ingredients) if ingredients else "active ingredients"
    
    # Rule-based descriptions
    descriptions = {
        "brightening": f"Helps illuminate and even out skin tone using {ingredient_str}.",
        "fades dark spots": "Targets hyperpigmentation and helps reduce the appearance of dark spots over time.",
        "hydrating": f"Provides deep moisture to keep skin plump and hydrated.",
        "anti-aging": "Helps reduce the appearance of fine lines and wrinkles.",
        "smoothing": "Helps refine skin texture for a smoother appearance.",
        "firming": "Supports skin elasticity and firmness.",
        "soothing": "Calms and comforts irritated or sensitive skin.",
        "pore minimizing": "Helps reduce the appearance of enlarged pores.",
        "acne control": "Helps prevent and treat acne breakouts.",
        "oil control": "Helps regulate excess sebum production."
    }
    
    # Find matching description or generate generic one
    for key, desc in descriptions.items():
        if key in benefit_lower:
            return desc
    
    # Generic fallback
    return f"Contributes to overall skin health and appearance."


def _generate_benefits_summary(product_name: str, benefits: List[str]) -> str:
    """Generate a summary of all benefits."""
    if not benefits:
        return f"{product_name} is designed to improve overall skin health."
    
    if len(benefits) == 1:
        return f"{product_name} focuses on {benefits[0].lower()} for improved skin appearance."
    
    benefits_str = ", ".join(benefits[:-1]).lower()
    last_benefit = benefits[-1].lower()
    
    return f"{product_name} offers multiple benefits including {benefits_str} and {last_benefit}."


# =============================================================================
# STANDALONE EXECUTION (for testing)
# =============================================================================

if __name__ == "__main__":
    import json
    
    sample_product = {
        "name": "GlowBoost Vitamin C Serum",
        "ingredients": ["Vitamin C", "Hyaluronic Acid"],
        "benefits": ["Brightening", "Fades dark spots"]
    }
    
    result = generate_benefits(sample_product)
    print("Benefits Block Test")
    print("=" * 50)
    print(json.dumps(result, indent=2))
