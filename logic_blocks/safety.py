"""
Safety Logic Block
==================
Pure function to generate safety content from product data.
"""

from typing import Dict, Any, List


def generate_safety(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate safety content block from product data.
    
    This is a pure function that transforms product safety data
    into a structured content fragment.
    
    Args:
        product: Parsed product object containing 'side_effects' field
        
    Returns:
        Structured safety content fragment
        
    Example Output:
        {
            "type": "safety",
            "title": "Safety Information",
            "side_effects": "...",
            "warnings": [...],
            "precautions": [...],
            "patch_test_recommended": true
        }
    """
    side_effects = product.get("side_effects", "")
    product_name = product.get("name", "This product")
    ingredients = product.get("ingredients", [])
    concentration = product.get("concentration", 0)
    
    # Parse side effects
    parsed_effects = _parse_side_effects(side_effects)
    
    # Generate warnings based on ingredients and concentration
    warnings = _generate_warnings(ingredients, concentration)
    
    # Generate precautions
    precautions = _generate_precautions(product_name, side_effects, ingredients)
    
    # Determine if patch test is recommended
    patch_test = _should_recommend_patch_test(side_effects, ingredients)
    
    return {
        "type": "safety",
        "title": "Safety Information",
        "product_name": product_name,
        "side_effects": {
            "description": side_effects,
            "severity": _assess_severity(side_effects),
            "details": parsed_effects
        },
        "warnings": warnings,
        "precautions": precautions,
        "patch_test_recommended": patch_test,
        "consultation_advised": _should_consult_dermatologist(side_effects, ingredients)
    }


def _parse_side_effects(side_effects: str) -> List[Dict[str, str]]:
    """Parse side effects text into structured list."""
    if not side_effects:
        return []
    
    effects = []
    
    # Common side effect keywords to look for
    effect_keywords = {
        "tingling": "Tingling sensation",
        "redness": "Skin redness",
        "irritation": "Skin irritation",
        "dryness": "Dryness",
        "peeling": "Skin peeling",
        "sensitivity": "Increased sensitivity",
        "burning": "Burning sensation",
        "itching": "Itching"
    }
    
    side_effects_lower = side_effects.lower()
    
    for keyword, name in effect_keywords.items():
        if keyword in side_effects_lower:
            effects.append({
                "effect": name,
                "likelihood": "possible" if "mild" in side_effects_lower else "common"
            })
    
    # If no specific effects found, add generic entry
    if not effects and side_effects:
        effects.append({
            "effect": side_effects,
            "likelihood": "as described"
        })
    
    return effects


def _generate_warnings(ingredients: List[str], concentration: float) -> List[str]:
    """Generate warnings based on ingredients and concentration."""
    warnings = []
    
    # Vitamin C specific warnings
    if any("vitamin c" in ing.lower() for ing in ingredients):
        warnings.append("Avoid using with other Vitamin C products to prevent irritation.")
        if concentration > 15:
            warnings.append("High concentration formula - start with less frequent application.")
    
    # Acid-related warnings
    acid_ingredients = ["glycolic", "salicylic", "lactic", "hyaluronic"]
    if any(acid in " ".join(ingredients).lower() for acid in acid_ingredients):
        warnings.append("May increase sun sensitivity - use sunscreen during the day.")
    
    # Retinol warnings
    if any("retinol" in ing.lower() or "retinoid" in ing.lower() for ing in ingredients):
        warnings.append("Not recommended for use during pregnancy.")
        warnings.append("Avoid combining with other retinoids or exfoliating acids.")
    
    # General warnings if none specific
    if not warnings:
        warnings.append("Discontinue use if irritation occurs.")
    
    return warnings


def _generate_precautions(
    product_name: str, 
    side_effects: str, 
    ingredients: List[str]
) -> List[str]:
    """Generate usage precautions."""
    precautions = []
    
    # Sensitive skin precaution
    if "sensitive" in side_effects.lower():
        precautions.append("Those with sensitive skin should perform a patch test first.")
    
    # General precautions
    precautions.extend([
        "For external use only.",
        "Avoid contact with eyes.",
        "Keep out of reach of children.",
        "Store in a cool, dry place away from direct sunlight."
    ])
    
    return precautions


def _assess_severity(side_effects: str) -> str:
    """Assess the severity level of side effects."""
    if not side_effects:
        return "none_reported"
    
    side_effects_lower = side_effects.lower()
    
    if any(word in side_effects_lower for word in ["severe", "serious", "dangerous"]):
        return "high"
    elif any(word in side_effects_lower for word in ["moderate", "significant"]):
        return "moderate"
    elif any(word in side_effects_lower for word in ["mild", "slight", "minor"]):
        return "mild"
    else:
        return "low"


def _should_recommend_patch_test(side_effects: str, ingredients: List[str]) -> bool:
    """Determine if patch test should be recommended."""
    # Always recommend for sensitive skin mentions
    if "sensitive" in side_effects.lower():
        return True
    
    # Recommend for active ingredients
    active_ingredients = ["vitamin c", "retinol", "glycolic", "salicylic", "aha", "bha"]
    if any(active in " ".join(ingredients).lower() for active in active_ingredients):
        return True
    
    return True  # Generally safe to always recommend


def _should_consult_dermatologist(side_effects: str, ingredients: List[str]) -> bool:
    """Determine if dermatologist consultation is advised."""
    # Recommend for strong actives or concerning side effects
    concerning_terms = ["severe", "allergic", "reaction", "medical", "condition"]
    
    return any(term in side_effects.lower() for term in concerning_terms)


# =============================================================================
# STANDALONE EXECUTION (for testing)
# =============================================================================

if __name__ == "__main__":
    import json
    
    sample_product = {
        "name": "GlowBoost Vitamin C Serum",
        "side_effects": "Mild tingling for sensitive skin",
        "ingredients": ["Vitamin C", "Hyaluronic Acid"],
        "concentration": 10.0
    }
    
    result = generate_safety(sample_product)
    print("Safety Block Test")
    print("=" * 50)
    print(json.dumps(result, indent=2))
