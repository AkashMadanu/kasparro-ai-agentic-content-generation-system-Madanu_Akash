"""
Usage Logic Block
=================
Pure function to generate usage content from product data.
"""

from typing import Dict, Any, List


def generate_usage(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate usage content block from product data.
    
    This is a pure function that transforms product usage data
    into a structured content fragment.
    
    Args:
        product: Parsed product object containing 'usage' field
        
    Returns:
        Structured usage content fragment
        
    Example Output:
        {
            "type": "usage",
            "title": "How to Use",
            "instructions": "...",
            "steps": [...],
            "tips": [...],
            "frequency": "..."
        }
    """
    usage_text = product.get("usage", "")
    product_name = product.get("name", "This product")
    skin_types = product.get("skin_type", [])
    
    # Parse usage into steps
    steps = _parse_usage_steps(usage_text)
    
    # Generate usage tips based on product data
    tips = _generate_usage_tips(product_name, skin_types, usage_text)
    
    # Determine frequency
    frequency = _determine_frequency(usage_text)
    
    return {
        "type": "usage",
        "title": "How to Use",
        "product_name": product_name,
        "instructions": usage_text,
        "steps": steps,
        "step_count": len(steps),
        "tips": tips,
        "frequency": frequency,
        "suitable_for": skin_types
    }


def _parse_usage_steps(usage_text: str) -> List[Dict[str, str]]:
    """
    Parse usage instructions into numbered steps.
    
    Attempts to break down usage text into discrete steps.
    """
    if not usage_text:
        return []
    
    steps = []
    
    # Common step indicators
    step_indicators = ["1.", "2.", "3.", "step 1", "step 2", "first", "then", "after"]
    
    # Check if text has natural steps
    has_steps = any(ind in usage_text.lower() for ind in step_indicators)
    
    if has_steps:
        # Split by common delimiters
        parts = usage_text.replace(". ", ".|").split("|")
        for i, part in enumerate(parts):
            if part.strip():
                steps.append({
                    "step_number": i + 1,
                    "instruction": part.strip()
                })
    else:
        # Create single comprehensive step
        steps.append({
            "step_number": 1,
            "instruction": usage_text
        })
    
    return steps


def _generate_usage_tips(
    product_name: str, 
    skin_types: List[str], 
    usage_text: str
) -> List[str]:
    """Generate helpful usage tips based on product data."""
    tips = []
    usage_lower = usage_text.lower()
    
    # Time-based tips
    if "morning" in usage_lower:
        tips.append("Use as part of your morning skincare routine for best results.")
    if "night" in usage_lower or "evening" in usage_lower:
        tips.append("Apply at night to allow the product to work while you sleep.")
    if "sunscreen" in usage_lower:
        tips.append("Always follow with sunscreen during the day for optimal protection.")
    
    # Application tips
    if "drops" in usage_lower:
        tips.append("Warm the drops between your palms before applying for better absorption.")
    
    # Skin type specific tips
    if skin_types:
        skin_str = " and ".join(skin_types).lower()
        tips.append(f"Specially formulated for {skin_str} skin types.")
    
    # General tip if no specific tips generated
    if not tips:
        tips.append("Apply to clean, dry skin for optimal absorption.")
        tips.append("Allow the product to fully absorb before applying other products.")
    
    return tips


def _determine_frequency(usage_text: str) -> str:
    """Determine recommended usage frequency from text."""
    usage_lower = usage_text.lower()
    
    if "twice" in usage_lower or "2x" in usage_lower:
        return "Twice daily (morning and evening)"
    elif "morning" in usage_lower and "night" not in usage_lower:
        return "Once daily (morning)"
    elif "night" in usage_lower or "evening" in usage_lower:
        return "Once daily (evening)"
    elif "daily" in usage_lower:
        return "Once daily"
    else:
        return "As directed"


# =============================================================================
# STANDALONE EXECUTION (for testing)
# =============================================================================

if __name__ == "__main__":
    import json
    
    sample_product = {
        "name": "GlowBoost Vitamin C Serum",
        "usage": "Apply 2–3 drops in the morning before sunscreen",
        "skin_type": ["Oily", "Combination"]
    }
    
    result = generate_usage(sample_product)
    print("Usage Block Test")
    print("=" * 50)
    print(json.dumps(result, indent=2))
