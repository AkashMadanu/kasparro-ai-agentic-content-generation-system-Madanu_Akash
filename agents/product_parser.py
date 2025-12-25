"""
ProductParserAgent
==================
Agent 1: Normalize and validate raw product JSON data.

Responsibility:
- Parse raw product data from JSON
- Normalize field names and values
- Extract numeric values from strings (price, concentration)
- Generate unique product ID
- Validate against schema

Input: Raw product JSON (from file or dict)
Output: Clean, normalized product object
LLM Usage: No (pure data transformation)
"""

import re
import uuid
import json
from typing import Dict, Any, Union
from pathlib import Path
from jsonschema import validate, ValidationError

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import PRODUCT_INPUT_SCHEMA, PARSED_PRODUCT_SCHEMA


class ProductParserAgent:
    """
    Agent responsible for parsing and normalizing raw product data.
    
    This agent performs pure data transformation without LLM calls.
    It ensures consistent data structure for downstream agents.
    """
    
    def __init__(self):
        """Initialize the ProductParserAgent."""
        self.name = "ProductParserAgent"
        self.input_schema = PRODUCT_INPUT_SCHEMA
        self.output_schema = PARSED_PRODUCT_SCHEMA
    
    def parse(self, input_data: Union[str, Path, Dict]) -> Dict[str, Any]:
        """
        Parse and normalize product data.
        
        Args:
            input_data: Either a file path (str/Path) or a dictionary
            
        Returns:
            Normalized product dictionary
            
        Raises:
            ValueError: If input data is invalid
            FileNotFoundError: If input file doesn't exist
        """
        # Load raw data
        raw_data = self._load_data(input_data)
        
        # Validate input schema
        self._validate_input(raw_data)
        
        # Normalize the data
        normalized = self._normalize(raw_data)
        
        # Validate output schema
        self._validate_output(normalized)
        
        return normalized
    
    def _load_data(self, input_data: Union[str, Path, Dict]) -> Dict[str, Any]:
        """Load data from file path or return dict directly."""
        if isinstance(input_data, dict):
            return input_data
        
        file_path = Path(input_data)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _validate_input(self, data: Dict[str, Any]) -> None:
        """Validate input data against schema."""
        try:
            validate(instance=data, schema=self.input_schema)
        except ValidationError as e:
            raise ValueError(f"Invalid input data: {e.message}")
    
    def _validate_output(self, data: Dict[str, Any]) -> None:
        """Validate output data against schema."""
        try:
            validate(instance=data, schema=self.output_schema)
        except ValidationError as e:
            raise ValueError(f"Invalid output data: {e.message}")
    
    def _normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize raw product data into clean internal model.
        
        Transformations:
        - Generate unique ID
        - Rename fields to consistent names
        - Extract numeric values from strings
        - Ensure arrays are properly formatted
        """
        return {
            "id": self._generate_id(raw.get("product_name", "")),
            "name": raw.get("product_name", "").strip(),
            "concentration": self._extract_concentration(raw.get("concentration", "")),
            "skin_type": self._normalize_array(raw.get("skin_type", [])),
            "ingredients": self._normalize_array(raw.get("key_ingredients", [])),
            "benefits": self._normalize_array(raw.get("benefits", [])),
            "usage": raw.get("how_to_use", "").strip(),
            "side_effects": raw.get("side_effects", "").strip(),
            "price": self._extract_price(raw.get("price", ""))
        }
    
    def _generate_id(self, name: str) -> str:
        """Generate a unique product ID based on name."""
        # Create slug from name
        slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        # Add short UUID for uniqueness
        short_uuid = str(uuid.uuid4())[:8]
        return f"{slug}-{short_uuid}"
    
    def _extract_concentration(self, value: str) -> float:
        """
        Extract numeric concentration value from string.
        
        Examples:
        - "10% Vitamin C" -> 10.0
        - "5%" -> 5.0
        - "15.5% Active" -> 15.5
        """
        if isinstance(value, (int, float)):
            return float(value)
        
        # Extract first number from string
        match = re.search(r'(\d+(?:\.\d+)?)', str(value))
        if match:
            return float(match.group(1))
        return 0.0
    
    def _extract_price(self, value: str) -> float:
        """
        Extract numeric price value from string.
        
        Examples:
        - "₹699" -> 699.0
        - "$29.99" -> 29.99
        - "1,299" -> 1299.0
        """
        if isinstance(value, (int, float)):
            return float(value)
        
        # Remove currency symbols and commas
        cleaned = re.sub(r'[₹$€£,\s]', '', str(value))
        
        # Extract number
        match = re.search(r'(\d+(?:\.\d+)?)', cleaned)
        if match:
            return float(match.group(1))
        return 0.0
    
    def _normalize_array(self, value: Any) -> list:
        """
        Normalize array values.
        
        - If already a list, clean each item
        - If string, split by comma
        - Remove empty items
        """
        if isinstance(value, list):
            return [item.strip() for item in value if item and str(item).strip()]
        
        if isinstance(value, str):
            items = value.split(',')
            return [item.strip() for item in items if item.strip()]
        
        return []
    
    def __repr__(self) -> str:
        return f"<{self.name}>"


# =============================================================================
# STANDALONE EXECUTION (for testing)
# =============================================================================

if __name__ == "__main__":
    # Test with sample data
    sample_data = {
        "product_name": "GlowBoost Vitamin C Serum",
        "concentration": "10% Vitamin C",
        "skin_type": ["Oily", "Combination"],
        "key_ingredients": ["Vitamin C", "Hyaluronic Acid"],
        "benefits": ["Brightening", "Fades dark spots"],
        "how_to_use": "Apply 2–3 drops in the morning before sunscreen",
        "side_effects": "Mild tingling for sensitive skin",
        "price": "₹699"
    }
    
    agent = ProductParserAgent()
    result = agent.parse(sample_data)
    
    print("ProductParserAgent Test")
    print("=" * 50)
    print(json.dumps(result, indent=2))
