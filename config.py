"""
Kasparro AI - Configuration Management
======================================
Centralized configuration for the Multi-Agent Content Generation System.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

# Base directory of the project
BASE_DIR = Path(__file__).parent.absolute()

# Directory paths
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / os.getenv("OUTPUT_DIR", "outputs")
TEMPLATES_DIR = BASE_DIR / "templates"
DOCS_DIR = BASE_DIR / "docs"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)

# =============================================================================
# LLM CONFIGURATION (Google Gemini)
# =============================================================================

# API Key (Required)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found! Please set it in your .env file.\n"
        "Get your API key from: https://aistudio.google.com/app/apikey"
    )

# Model selection
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Generation parameters
LLM_CONFIG = {
    "temperature": 0.3,  # Lower = more deterministic/consistent output
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 4096,
}

# =============================================================================
# AGENT CONFIGURATION
# =============================================================================

# Question generation settings
QUESTION_CATEGORIES = [
    "informational",
    "usage", 
    "safety",
    "purchase",
    "comparison"
]

MIN_QUESTIONS_PER_CATEGORY = 3
TOTAL_MIN_QUESTIONS = 15

# FAQ settings
MIN_FAQ_ITEMS = 5

# =============================================================================
# OUTPUT FILE NAMES
# =============================================================================

OUTPUT_FILES = {
    "faq": "faq.json",
    "product_page": "product_page.json",
    "comparison_page": "comparison_page.json"
}

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Console colors (using colorama)
COLORS = {
    "header": "\033[95m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "end": "\033[0m",
    "bold": "\033[1m",
}

# =============================================================================
# PRODUCT SCHEMA
# =============================================================================

PRODUCT_INPUT_SCHEMA = {
    "type": "object",
    "required": [
        "product_name",
        "concentration", 
        "skin_type",
        "key_ingredients",
        "benefits",
        "how_to_use",
        "side_effects",
        "price"
    ],
    "properties": {
        "product_name": {"type": "string"},
        "concentration": {"type": "string"},
        "skin_type": {
            "type": "array",
            "items": {"type": "string"}
        },
        "key_ingredients": {
            "type": "array", 
            "items": {"type": "string"}
        },
        "benefits": {
            "type": "array",
            "items": {"type": "string"}
        },
        "how_to_use": {"type": "string"},
        "side_effects": {"type": "string"},
        "price": {"type": "string"}
    }
}

PARSED_PRODUCT_SCHEMA = {
    "type": "object",
    "required": [
        "id",
        "name",
        "concentration",
        "skin_type",
        "ingredients",
        "benefits",
        "usage",
        "side_effects",
        "price"
    ],
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "concentration": {"type": "number"},
        "skin_type": {
            "type": "array",
            "items": {"type": "string"}
        },
        "ingredients": {
            "type": "array",
            "items": {"type": "string"}
        },
        "benefits": {
            "type": "array",
            "items": {"type": "string"}
        },
        "usage": {"type": "string"},
        "side_effects": {"type": "string"},
        "price": {"type": "number"}
    }
}
