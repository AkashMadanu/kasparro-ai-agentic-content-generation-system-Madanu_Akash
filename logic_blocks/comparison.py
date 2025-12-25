"""
Comparison Logic Block
======================
Pure function to compare two products and generate comparison content.
"""

from typing import Dict, Any, List


def compare_products(
    product_a: Dict[str, Any], 
    product_b: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Compare two products and generate comparison content.
    
    This is a pure function that analyzes two products
    and produces a structured comparison.
    
    Args:
        product_a: First product object
        product_b: Second product object
        
    Returns:
        Structured comparison content fragment
        
    Example Output:
        {
            "type": "comparison",
            "products": ["Product A", "Product B"],
            "dimensions": {
                "ingredients": {...},
                "benefits": {...},
                "price": {...}
            }
        }
    """
    name_a = product_a.get("name", "Product A")
    name_b = product_b.get("name", "Product B")
    
    # Compare each dimension
    ingredients_comparison = _compare_ingredients(product_a, product_b)
    benefits_comparison = _compare_benefits(product_a, product_b)
    price_comparison = _compare_price(product_a, product_b)
    skin_type_comparison = _compare_skin_types(product_a, product_b)
    
    # Determine overall winner for each category
    scores = _calculate_scores(
        ingredients_comparison,
        benefits_comparison,
        price_comparison
    )
    
    return {
        "type": "comparison",
        "products": {
            "product_a": name_a,
            "product_b": name_b
        },
        "dimensions": {
            "ingredients": ingredients_comparison,
            "benefits": benefits_comparison,
            "price": price_comparison,
            "skin_type": skin_type_comparison
        },
        "scores": scores,
        "summary": _generate_comparison_summary(name_a, name_b, scores)
    }


def _compare_ingredients(
    product_a: Dict[str, Any], 
    product_b: Dict[str, Any]
) -> Dict[str, Any]:
    """Compare ingredients between two products."""
    ing_a = set(i.lower() for i in product_a.get("ingredients", []))
    ing_b = set(i.lower() for i in product_b.get("ingredients", []))
    
    common = ing_a.intersection(ing_b)
    unique_a = ing_a - ing_b
    unique_b = ing_b - ing_a
    
    return {
        "product_a": {
            "ingredients": product_a.get("ingredients", []),
            "count": len(product_a.get("ingredients", [])),
            "concentration": product_a.get("concentration", "N/A")
        },
        "product_b": {
            "ingredients": product_b.get("ingredients", []),
            "count": len(product_b.get("ingredients", [])),
            "concentration": product_b.get("concentration", "N/A")
        },
        "common_ingredients": list(common),
        "unique_to_a": list(unique_a),
        "unique_to_b": list(unique_b),
        "analysis": _analyze_ingredients(common, unique_a, unique_b)
    }


def _compare_benefits(
    product_a: Dict[str, Any], 
    product_b: Dict[str, Any]
) -> Dict[str, Any]:
    """Compare benefits between two products."""
    ben_a = set(b.lower() for b in product_a.get("benefits", []))
    ben_b = set(b.lower() for b in product_b.get("benefits", []))
    
    common = ben_a.intersection(ben_b)
    unique_a = ben_a - ben_b
    unique_b = ben_b - ben_a
    
    return {
        "product_a": {
            "benefits": product_a.get("benefits", []),
            "count": len(product_a.get("benefits", []))
        },
        "product_b": {
            "benefits": product_b.get("benefits", []),
            "count": len(product_b.get("benefits", []))
        },
        "common_benefits": list(common),
        "unique_to_a": list(unique_a),
        "unique_to_b": list(unique_b),
        "analysis": _analyze_benefits(common, unique_a, unique_b)
    }


def _compare_price(
    product_a: Dict[str, Any], 
    product_b: Dict[str, Any]
) -> Dict[str, Any]:
    """Compare pricing between two products."""
    price_a = _extract_price(product_a.get("price", 0))
    price_b = _extract_price(product_b.get("price", 0))
    
    difference = abs(price_a - price_b)
    percentage_diff = (difference / max(price_a, price_b) * 100) if max(price_a, price_b) > 0 else 0
    
    cheaper = None
    if price_a < price_b:
        cheaper = "product_a"
    elif price_b < price_a:
        cheaper = "product_b"
    
    return {
        "product_a": {
            "price": price_a,
            "formatted": f"₹{price_a}"
        },
        "product_b": {
            "price": price_b,
            "formatted": f"₹{price_b}"
        },
        "difference": difference,
        "percentage_difference": round(percentage_diff, 1),
        "cheaper_option": cheaper,
        "analysis": _analyze_price(price_a, price_b, cheaper)
    }


def _compare_skin_types(
    product_a: Dict[str, Any], 
    product_b: Dict[str, Any]
) -> Dict[str, Any]:
    """Compare target skin types between two products."""
    types_a = set(t.lower() for t in product_a.get("skin_type", []))
    types_b = set(t.lower() for t in product_b.get("skin_type", []))
    
    common = types_a.intersection(types_b)
    
    return {
        "product_a": product_a.get("skin_type", []),
        "product_b": product_b.get("skin_type", []),
        "common_skin_types": list(common),
        "analysis": f"Both products target {len(common)} common skin type(s)." if common else "Products target different skin types."
    }


def _extract_price(price_value: Any) -> float:
    """Extract numeric price from various formats."""
    if isinstance(price_value, (int, float)):
        return float(price_value)
    
    if isinstance(price_value, str):
        import re
        # Remove currency symbols and commas
        cleaned = re.sub(r'[₹$€£,\s]', '', price_value)
        match = re.search(r'(\d+(?:\.\d+)?)', cleaned)
        if match:
            return float(match.group(1))
    
    return 0.0


def _analyze_ingredients(
    common: set, 
    unique_a: set, 
    unique_b: set
) -> str:
    """Generate analysis text for ingredient comparison."""
    if common:
        return f"Products share {len(common)} common ingredient(s), suggesting similar formulation approaches."
    elif unique_a and unique_b:
        return "Products have completely different ingredient profiles, catering to different skincare needs."
    else:
        return "Limited ingredient overlap between products."


def _analyze_benefits(
    common: set, 
    unique_a: set, 
    unique_b: set
) -> str:
    """Generate analysis text for benefits comparison."""
    if common:
        return f"Both products offer {len(common)} similar benefit(s), making them comparable choices."
    else:
        return "Products offer different benefits and may serve different skincare goals."


def _analyze_price(price_a: float, price_b: float, cheaper: str) -> str:
    """Generate analysis text for price comparison."""
    if price_a == price_b:
        return "Both products are priced equally, so choice can be based on other factors."
    elif cheaper == "product_a":
        return "Product A offers a more budget-friendly option."
    else:
        return "Product B offers a more budget-friendly option."


def _calculate_scores(
    ingredients: Dict, 
    benefits: Dict, 
    price: Dict
) -> Dict[str, Any]:
    """Calculate comparison scores for each product."""
    score_a = 0
    score_b = 0
    
    # Ingredients score (based on count and uniqueness)
    if ingredients["product_a"]["count"] > ingredients["product_b"]["count"]:
        score_a += 1
    elif ingredients["product_b"]["count"] > ingredients["product_a"]["count"]:
        score_b += 1
    
    # Benefits score
    if benefits["product_a"]["count"] > benefits["product_b"]["count"]:
        score_a += 1
    elif benefits["product_b"]["count"] > benefits["product_a"]["count"]:
        score_b += 1
    
    # Price score (lower is better)
    if price["cheaper_option"] == "product_a":
        score_a += 1
    elif price["cheaper_option"] == "product_b":
        score_b += 1
    
    return {
        "product_a_score": score_a,
        "product_b_score": score_b,
        "winner": "product_a" if score_a > score_b else ("product_b" if score_b > score_a else "tie")
    }


def _generate_comparison_summary(
    name_a: str, 
    name_b: str, 
    scores: Dict
) -> str:
    """Generate overall comparison summary."""
    if scores["winner"] == "tie":
        return f"{name_a} and {name_b} are closely matched products. Your choice may depend on specific preferences and skin needs."
    elif scores["winner"] == "product_a":
        return f"{name_a} edges ahead in this comparison based on ingredients, benefits, and price factors."
    else:
        return f"{name_b} edges ahead in this comparison based on ingredients, benefits, and price factors."


# =============================================================================
# STANDALONE EXECUTION (for testing)
# =============================================================================

if __name__ == "__main__":
    import json
    
    product_a = {
        "name": "GlowBoost Vitamin C Serum",
        "ingredients": ["Vitamin C", "Hyaluronic Acid"],
        "benefits": ["Brightening", "Fades dark spots"],
        "price": 699,
        "skin_type": ["Oily", "Combination"]
    }
    
    product_b = {
        "name": "RadiantGlow Serum",
        "ingredients": ["Niacinamide", "Hyaluronic Acid", "Zinc"],
        "benefits": ["Pore minimizing", "Oil control", "Brightening"],
        "price": 599,
        "skin_type": ["Oily", "Acne-prone"]
    }
    
    result = compare_products(product_a, product_b)
    print("Comparison Block Test")
    print("=" * 50)
    print(json.dumps(result, indent=2))
