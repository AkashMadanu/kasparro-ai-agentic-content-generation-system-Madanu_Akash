"""
FAQPageAgent
============
Agent 5: Generate FAQ page with Q&As.

Responsibility:
- Use questions from QuestionGeneratorAgent
- Generate answers using ContentLogicAgent and LLM
- Apply FAQ template
- Output structured faq.json

Input: Questions + product data
Output: faq.json structure
LLM Usage: Yes (for answer generation)
"""

import json
from datetime import datetime, timezone
from typing import Dict, Any, List
from pathlib import Path

import google.generativeai as genai

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import GEMINI_API_KEY, GEMINI_MODEL, LLM_CONFIG, MIN_FAQ_ITEMS


class FAQPageAgent:
    """
    Agent responsible for generating the FAQ page.
    
    This agent takes questions from QuestionGeneratorAgent,
    generates answers using the product data and LLM,
    and outputs a structured FAQ page.
    """
    
    def __init__(self):
        """Initialize the FAQPageAgent with Gemini."""
        self.name = "FAQPageAgent"
        self.min_faqs = MIN_FAQ_ITEMS
        
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
    
    def generate(
        self, 
        product: Dict[str, Any],
        questions: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Generate the FAQ page.
        
        Args:
            product: Parsed product object
            questions: Categorized questions from QuestionGeneratorAgent
            
        Returns:
            Structured FAQ page JSON
        """
        # Select questions for FAQ (at least MIN_FAQ_ITEMS)
        selected_questions = self._select_questions(questions)
        
        # Generate answers for each question
        faqs = self._generate_answers(product, selected_questions)
        
        # Build final FAQ page structure
        faq_page = {
            "page_type": "faq",
            "product_name": product.get("name", ""),
            "product_id": product.get("id", ""),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_faqs": len(faqs),
            "faqs": faqs
        }
        
        return faq_page
    
    def _select_questions(
        self, 
        questions: Dict[str, List[str]]
    ) -> List[Dict[str, str]]:
        """
        Select questions for the FAQ page.
        
        Ensures diversity by selecting from multiple categories.
        """
        selected = []
        
        # Priority order for FAQ relevance
        category_priority = ["informational", "usage", "safety", "purchase", "comparison"]
        
        # First pass: get at least one from each category
        for category in category_priority:
            if category in questions and questions[category]:
                selected.append({
                    "question": questions[category][0],
                    "category": category
                })
        
        # Second pass: fill up to desired count
        for category in category_priority:
            if len(selected) >= self.min_faqs:
                break
            if category in questions:
                for q in questions[category][1:]:  # Skip first (already added)
                    if len(selected) >= self.min_faqs + 2:  # Get a few extra
                        break
                    selected.append({
                        "question": q,
                        "category": category
                    })
        
        return selected
    
    def _generate_answers(
        self, 
        product: Dict[str, Any],
        questions: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """Generate answers for selected questions using LLM."""
        prompt = self._build_prompt(product, questions)
        response = self._call_llm(prompt)
        return self._parse_response(response)
    
    def _build_prompt(
        self, 
        product: Dict[str, Any],
        questions: List[Dict[str, str]]
    ) -> str:
        """Build prompt for answer generation."""
        questions_text = "\n".join([
            f"{i+1}. [{q['category']}] {q['question']}"
            for i, q in enumerate(questions)
        ])
        
        return f"""You are the FAQPageAgent in a multi-agent content generation system.

Your task is to generate answers for FAQ questions about a skincare product.

PRODUCT DATA:
- Name: {product.get('name', '')}
- Concentration: {product.get('concentration', '')}%
- Skin Types: {', '.join(product.get('skin_type', []))}
- Key Ingredients: {', '.join(product.get('ingredients', []))}
- Benefits: {', '.join(product.get('benefits', []))}
- How to Use: {product.get('usage', '')}
- Side Effects: {product.get('side_effects', '')}
- Price: ₹{product.get('price', '')}

QUESTIONS TO ANSWER:
{questions_text}

REQUIREMENTS:
1. Answer each question based ONLY on the provided product data
2. Keep answers concise but informative (2-3 sentences)
3. Do NOT make up information not present in the product data
4. Include the category with each Q&A

OUTPUT FORMAT (strict JSON array):
{{
    "faqs": [
        {{
            "question": "the question",
            "answer": "your answer",
            "category": "category"
        }}
    ]
}}

Generate the answers now. Return ONLY valid JSON, no explanations."""
    
    def _call_llm(self, prompt: str) -> str:
        """Call Gemini API."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"LLM call failed: {str(e)}")
    
    def _parse_response(self, response: str) -> List[Dict[str, str]]:
        """Parse LLM response into FAQ list."""
        try:
            cleaned = response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            data = json.loads(cleaned.strip())
            return data.get("faqs", [])
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response: {str(e)}")
    
    def __repr__(self) -> str:
        return f"<{self.name} min_faqs={self.min_faqs}>"


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
    
    sample_questions = {
        "informational": ["What is GlowBoost Vitamin C Serum?", "What ingredients are in it?"],
        "usage": ["How do I apply the serum?", "When should I use it?"],
        "safety": ["Are there any side effects?", "Is it safe for sensitive skin?"],
        "purchase": ["How much does it cost?"],
        "comparison": ["How does it compare to other serums?"]
    }
    
    agent = FAQPageAgent()
    result = agent.generate(sample_product, sample_questions)
    
    print("FAQPageAgent Test")
    print("=" * 50)
    print(json.dumps(result, indent=2))
