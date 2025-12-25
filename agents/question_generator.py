"""
QuestionGeneratorAgent
======================
Agent 2: Generate categorized user questions from product data.

Responsibility:
- Generate at least 15 user questions about the product
- Categorize questions into: informational, usage, safety, purchase, comparison
- Use LLM to generate natural, relevant questions
- Return structured JSON output

Input: Parsed product object (from ProductParserAgent)
Output: Questions grouped by category
LLM Usage: Yes (Gemini 1.5 Flash)
"""

import json
from typing import Dict, Any, List
from pathlib import Path

import google.generativeai as genai

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import (
    GEMINI_API_KEY, 
    GEMINI_MODEL, 
    LLM_CONFIG,
    QUESTION_CATEGORIES,
    MIN_QUESTIONS_PER_CATEGORY,
    TOTAL_MIN_QUESTIONS
)


class QuestionGeneratorAgent:
    """
    Agent responsible for generating categorized user questions.
    
    This agent uses Gemini LLM to generate natural questions that
    users might ask about the product. Questions are categorized
    into predefined categories for structured output.
    """
    
    def __init__(self):
        """Initialize the QuestionGeneratorAgent with Gemini."""
        self.name = "QuestionGeneratorAgent"
        self.categories = QUESTION_CATEGORIES
        
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
    
    def generate(self, product: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Generate categorized questions for a product.
        
        Args:
            product: Parsed product object
            
        Returns:
            Dictionary with categories as keys and question lists as values
        """
        prompt = self._build_prompt(product)
        response = self._call_llm(prompt)
        questions = self._parse_response(response)
        
        # Validate minimum questions
        self._validate_questions(questions)
        
        return questions
    
    def _build_prompt(self, product: Dict[str, Any]) -> str:
        """Build the prompt for question generation."""
        return f"""You are the QuestionGeneratorAgent in a multi-agent content generation system.

Your task is to generate user questions about a skincare product.

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
1. Generate at least {TOTAL_MIN_QUESTIONS} questions total
2. Generate at least {MIN_QUESTIONS_PER_CATEGORY} questions per category
3. Questions must be based ONLY on the provided product data
4. Questions should be natural and what real users would ask
5. Do NOT include any information not present in the product data

CATEGORIES:
1. informational - Questions about what the product is, ingredients, general info
2. usage - Questions about how to use, application, routine
3. safety - Questions about side effects, precautions, skin reactions
4. purchase - Questions about price, value, where to buy
5. comparison - Questions comparing to other products or alternatives

OUTPUT FORMAT (strict JSON):
{{
    "informational": ["question1", "question2", "question3"],
    "usage": ["question1", "question2", "question3"],
    "safety": ["question1", "question2", "question3"],
    "purchase": ["question1", "question2", "question3"],
    "comparison": ["question1", "question2", "question3"]
}}

Generate the questions now. Return ONLY valid JSON, no explanations."""
    
    def _call_llm(self, prompt: str) -> str:
        """Call Gemini API and return response text."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"LLM call failed: {str(e)}")
    
    def _parse_response(self, response: str) -> Dict[str, List[str]]:
        """Parse LLM response into structured format."""
        try:
            # Clean response if needed
            cleaned = response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            data = json.loads(cleaned.strip())
            
            # Ensure all categories exist
            result = {}
            for category in self.categories:
                result[category] = data.get(category, [])
            
            return result
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response as JSON: {str(e)}")
    
    def _validate_questions(self, questions: Dict[str, List[str]]) -> None:
        """Validate that minimum questions are generated."""
        total = sum(len(q) for q in questions.values())
        
        if total < TOTAL_MIN_QUESTIONS:
            raise ValueError(
                f"Insufficient questions generated: {total} "
                f"(minimum: {TOTAL_MIN_QUESTIONS})"
            )
    
    def get_total_count(self, questions: Dict[str, List[str]]) -> int:
        """Get total question count across all categories."""
        return sum(len(q) for q in questions.values())
    
    def __repr__(self) -> str:
        return f"<{self.name} categories={self.categories}>"


# =============================================================================
# STANDALONE EXECUTION (for testing)
# =============================================================================

if __name__ == "__main__":
    # Test with sample parsed product
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
    
    agent = QuestionGeneratorAgent()
    result = agent.generate(sample_product)
    
    print("QuestionGeneratorAgent Test")
    print("=" * 50)
    print(json.dumps(result, indent=2))
    print(f"\nTotal questions: {agent.get_total_count(result)}")
