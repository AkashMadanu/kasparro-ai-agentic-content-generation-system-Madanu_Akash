"""
Ingredients Logic Block
=======================
Pure function to generate ingredients content from product data.
"""

from typing import Dict, Any, List


def generate_ingredients(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate ingredients content block from product data.
    
    This is a pure function that transforms product ingredients data
    into a structured content fragment.
    
    Args:
        product: Parsed product object containing 'ingredients' field
        
    Returns:
        Structured ingredients content fragment
        
    Example Output:
        {
            "type": "ingredients",
            "title": "Key Ingredients",
            "items": [
                {"name": "Vitamin C", "description": "...", "benefit": "..."},
                ...
            ],
            "concentration": "10%"
        }
    """
    ingredients = product.get("ingredients", [])
    product_name = product.get("name", "This product")
    concentration = product.get("concentration", 0)
    
    # Build detailed ingredient information
    items = []
    for ingredient in ingredients:
        items.append({
            "name": ingredient,
            "description": _get_ingredient_description(ingredient),
            "benefit": _get_ingredient_benefit(ingredient),
            "category": _categorize_ingredient(ingredient)
        })
    
    return {
        "type": "ingredients",
        "title": "Key Ingredients",
        "product_name": product_name,
        "count": len(items),
        "items": items,
        "concentration": f"{concentration}%" if concentration else "Not specified",
        "hero_ingredient": items[0]["name"] if items else None,
        "ingredient_summary": _generate_ingredient_summary(ingredients)
    }


def _get_ingredient_description(ingredient: str) -> str:
    """Get a description for a specific ingredient."""
    ingredient_lower = ingredient.lower()
    
    descriptions = {
        "vitamin c": "A powerful antioxidant that helps protect the skin from environmental damage and promotes collagen production.",
        "hyaluronic acid": "A naturally occurring molecule that attracts and retains moisture, helping to keep skin hydrated and plump.",
        "niacinamide": "Also known as Vitamin B3, it helps improve skin texture, minimize pores, and strengthen the skin barrier.",
        "retinol": "A form of Vitamin A that promotes cell turnover and collagen production for anti-aging benefits.",
        "salicylic acid": "A beta hydroxy acid (BHA) that penetrates pores to help clear acne and prevent breakouts.",
        "glycolic acid": "An alpha hydroxy acid (AHA) that exfoliates the skin surface for a smoother, brighter complexion.",
        "ceramides": "Lipids that help maintain the skin's barrier function and retain moisture.",
        "peptides": "Amino acid chains that signal the skin to produce more collagen and elastin.",
        "squalane": "A lightweight, non-comedogenic oil that hydrates and softens the skin.",
        "zinc": "A mineral that helps control oil production and has anti-inflammatory properties.",
        "aloe vera": "A soothing plant extract known for its hydrating and calming properties.",
        "green tea": "Rich in antioxidants, it helps protect against environmental stressors and soothes the skin."
    }
    
    for key, desc in descriptions.items():
        if key in ingredient_lower:
            return desc
    
    return f"An active ingredient that contributes to the product's effectiveness."


def _get_ingredient_benefit(ingredient: str) -> str:
    """Get the primary benefit of an ingredient."""
    ingredient_lower = ingredient.lower()
    
    benefits = {
        "vitamin c": "Brightening & antioxidant protection",
        "hyaluronic acid": "Deep hydration & plumping",
        "niacinamide": "Pore minimizing & barrier support",
        "retinol": "Anti-aging & cell renewal",
        "salicylic acid": "Acne control & pore cleansing",
        "glycolic acid": "Exfoliation & skin renewal",
        "ceramides": "Barrier repair & moisture retention",
        "peptides": "Firming & collagen support",
        "squalane": "Lightweight hydration",
        "zinc": "Oil control & anti-inflammatory",
        "aloe vera": "Soothing & hydrating",
        "green tea": "Antioxidant protection"
    }
    
    for key, benefit in benefits.items():
        if key in ingredient_lower:
            return benefit
    
    return "Skin health support"


def _categorize_ingredient(ingredient: str) -> str:
    """Categorize an ingredient by type."""
    ingredient_lower = ingredient.lower()
    
    categories = {
        "antioxidant": ["vitamin c", "vitamin e", "green tea", "resveratrol"],
        "hydrator": ["hyaluronic acid", "glycerin", "squalane", "aloe"],
        "exfoliant": ["glycolic", "salicylic", "lactic", "aha", "bha"],
        "anti-aging": ["retinol", "retinoid", "peptide", "collagen"],
        "soothing": ["aloe", "chamomile", "centella", "cica"],
        "vitamin": ["vitamin c", "vitamin e", "vitamin b", "niacinamide"],
        "acid": ["hyaluronic", "glycolic", "salicylic", "lactic"]
    }
    
    for category, keywords in categories.items():
        if any(kw in ingredient_lower for kw in keywords):
            return category
    
    return "active"


def _generate_ingredient_summary(ingredients: List[str]) -> str:
    """Generate a summary of all ingredients."""
    if not ingredients:
        return "No key ingredients specified."
    
    if len(ingredients) == 1:
        return f"Powered by {ingredients[0]} for targeted skincare benefits."
    
    return f"Formulated with {', '.join(ingredients[:-1])} and {ingredients[-1]} for comprehensive skincare benefits."


# =============================================================================
# STANDALONE EXECUTION (for testing)
# =============================================================================

if __name__ == "__main__":
    import json
    
    sample_product = {
        "name": "GlowBoost Vitamin C Serum",
        "ingredients": ["Vitamin C", "Hyaluronic Acid"],
        "concentration": 10.0
    }
    
    result = generate_ingredients(sample_product)
    print("Ingredients Block Test")
    print("=" * 50)
    print(json.dumps(result, indent=2))
