"""
Kasparro AI - Logic Blocks Package
==================================
Reusable content transformation functions.
"""

from .benefits import generate_benefits
from .usage import generate_usage
from .safety import generate_safety
from .ingredients import generate_ingredients
from .comparison import compare_products

__all__ = [
    "generate_benefits",
    "generate_usage",
    "generate_safety",
    "generate_ingredients",
    "compare_products"
]
