"""
Kasparro AI - Multi-Agent Content Generation System
===================================================
Main Orchestrator - DAG Pipeline Execution

This is the main entry point for the content generation pipeline.
It orchestrates all agents in a DAG (Directed Acyclic Graph) pattern.

Usage:
    python orchestrator.py input/product.json

Pipeline Flow:
    Input JSON → ProductParserAgent → QuestionGeneratorAgent → 
    [FAQPageAgent, ProductPageAgent, ComparisonAgent] → Output JSONs
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

from config import OUTPUT_DIR, OUTPUT_FILES, COLORS
from agents import (
    ProductParserAgent,
    QuestionGeneratorAgent,
    ContentLogicAgent,
    TemplateEngineAgent,
    FAQPageAgent,
    ProductPageAgent,
    ComparisonAgent
)


class Orchestrator:
    """
    Pipeline orchestrator for the Multi-Agent Content Generation System.
    
    Manages the execution flow of all agents in a DAG pattern,
    ensuring proper data flow between agents.
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize the orchestrator.
        
        Args:
            verbose: Whether to print progress messages
        """
        self.verbose = verbose
        self.output_dir = OUTPUT_DIR
        
        # Initialize all agents
        self.agents = {
            "parser": ProductParserAgent(),
            "question_generator": QuestionGeneratorAgent(),
            "content_logic": ContentLogicAgent(),
            "template_engine": TemplateEngineAgent(),
            "faq": FAQPageAgent(),
            "product_page": ProductPageAgent(),
            "comparison": ComparisonAgent()
        }
        
        # Pipeline state
        self.state = {
            "raw_product": None,
            "parsed_product": None,
            "questions": None,
            "content_blocks": None,
            "faq_page": None,
            "product_page": None,
            "comparison_page": None
        }
    
    def run(self, input_path: str) -> Dict[str, Any]:
        """
        Execute the complete pipeline.
        
        Args:
            input_path: Path to input product JSON file
            
        Returns:
            Dictionary containing all generated outputs
        """
        self._print_header()
        start_time = datetime.now()
        
        try:
            # Stage 1: Parse product data
            self._execute_stage(
                1, "ProductParserAgent", "Parsing product data...",
                self._stage_parse_product, input_path
            )
            
            # Stage 2: Generate questions
            self._execute_stage(
                2, "QuestionGeneratorAgent", "Generating categorized questions...",
                self._stage_generate_questions
            )
            
            # Stage 3: Prepare content logic blocks
            self._execute_stage(
                3, "ContentLogicAgent", "Preparing content logic blocks...",
                self._stage_prepare_content_blocks
            )
            
            # Stage 4: Load templates
            self._execute_stage(
                4, "TemplateEngineAgent", "Loading templates...",
                self._stage_load_templates
            )
            
            # Stage 5: Generate FAQ page
            self._execute_stage(
                5, "FAQPageAgent", "Generating FAQ page...",
                self._stage_generate_faq
            )
            
            # Stage 6: Generate Product page
            self._execute_stage(
                6, "ProductPageAgent", "Generating product page...",
                self._stage_generate_product_page
            )
            
            # Stage 7: Generate Comparison page
            self._execute_stage(
                7, "ComparisonAgent", "Creating comparison page...",
                self._stage_generate_comparison
            )
            
            # Write outputs
            self._write_outputs()
            
            # Print summary
            elapsed = (datetime.now() - start_time).total_seconds()
            self._print_summary(elapsed)
            
            return {
                "success": True,
                "outputs": {
                    "faq": str(self.output_dir / OUTPUT_FILES["faq"]),
                    "product_page": str(self.output_dir / OUTPUT_FILES["product_page"]),
                    "comparison_page": str(self.output_dir / OUTPUT_FILES["comparison_page"])
                },
                "elapsed_time": elapsed
            }
            
        except Exception as e:
            self._print_error(str(e))
            return {
                "success": False,
                "error": str(e)
            }
    
    def _execute_stage(
        self, 
        stage_num: int, 
        agent_name: str, 
        description: str,
        stage_func,
        *args
    ):
        """Execute a pipeline stage with logging."""
        self._print_stage(stage_num, agent_name, description)
        result = stage_func(*args)
        return result
    
    # =========================================================================
    # Pipeline Stages
    # =========================================================================
    
    def _stage_parse_product(self, input_path: str):
        """Stage 1: Parse product data."""
        self.state["parsed_product"] = self.agents["parser"].parse(input_path)
        product_name = self.state["parsed_product"].get("name", "Unknown")
        self._print_success(f"Product parsed: {product_name}")
    
    def _stage_generate_questions(self):
        """Stage 2: Generate categorized questions."""
        self.state["questions"] = self.agents["question_generator"].generate(
            self.state["parsed_product"]
        )
        total = self.agents["question_generator"].get_total_count(self.state["questions"])
        categories = len(self.state["questions"])
        self._print_success(f"Generated {total} questions across {categories} categories")
    
    def _stage_prepare_content_blocks(self):
        """Stage 3: Prepare content logic blocks."""
        self.state["content_blocks"] = self.agents["content_logic"].get_all_blocks(
            self.state["parsed_product"]
        )
        self._print_success("Logic blocks ready")
    
    def _stage_load_templates(self):
        """Stage 4: Load templates."""
        templates = self.agents["template_engine"].list_templates()
        self._print_success(f"Templates loaded: {', '.join(t.upper() for t in templates)}")
    
    def _stage_generate_faq(self):
        """Stage 5: Generate FAQ page."""
        self.state["faq_page"] = self.agents["faq"].generate(
            self.state["parsed_product"],
            self.state["questions"]
        )
        faq_count = len(self.state["faq_page"].get("faqs", []))
        self._print_success(f"FAQ page generated with {faq_count} Q&As")
    
    def _stage_generate_product_page(self):
        """Stage 6: Generate Product page."""
        self.state["product_page"] = self.agents["product_page"].generate(
            self.state["parsed_product"]
        )
        self._print_success("Product page generated")
    
    def _stage_generate_comparison(self):
        """Stage 7: Generate Comparison page."""
        self.state["comparison_page"] = self.agents["comparison"].generate(
            self.state["parsed_product"]
        )
        product_b_name = self.state["comparison_page"].get("product_b", {}).get("name", "Product B")
        self._print_success(f"Comparison page generated (vs {product_b_name})")
    
    # =========================================================================
    # Output Writing
    # =========================================================================
    
    def _write_outputs(self):
        """Write all output JSON files."""
        self.output_dir.mkdir(exist_ok=True)
        
        outputs = [
            (OUTPUT_FILES["faq"], self.state["faq_page"]),
            (OUTPUT_FILES["product_page"], self.state["product_page"]),
            (OUTPUT_FILES["comparison_page"], self.state["comparison_page"])
        ]
        
        for filename, data in outputs:
            filepath = self.output_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
    
    # =========================================================================
    # Console Output Helpers
    # =========================================================================
    
    def _print_header(self):
        """Print pipeline header."""
        if not self.verbose:
            return
        print()
        print("═" * 67)
        print("       KASPARRO AI - Multi-Agent Content Generation System")
        print("═" * 67)
        print()
    
    def _print_stage(self, num: int, agent: str, desc: str):
        """Print stage information."""
        if not self.verbose:
            return
        print(f"[{num}/7] {agent}: {desc}")
    
    def _print_success(self, message: str):
        """Print success message."""
        if not self.verbose:
            return
        print(f"      ✓ {message}")
        print()
    
    def _print_error(self, message: str):
        """Print error message."""
        print()
        print(f"✗ ERROR: {message}")
        print()
    
    def _print_summary(self, elapsed: float):
        """Print pipeline summary."""
        if not self.verbose:
            return
        print("═" * 67)
        print("                         OUTPUT FILES")
        print("═" * 67)
        print(f"  • {self.output_dir / OUTPUT_FILES['faq']}")
        print(f"  • {self.output_dir / OUTPUT_FILES['product_page']}")
        print(f"  • {self.output_dir / OUTPUT_FILES['comparison_page']}")
        print()
        print(f"✓ Pipeline completed successfully! (Time: {elapsed:.2f}s)")
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Kasparro AI - Multi-Agent Content Generation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python orchestrator.py input/product.json
  python orchestrator.py path/to/custom_product.json --quiet
        """
    )
    
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to input product JSON file"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress output"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default=None,
        help="Custom output directory"
    )
    
    args = parser.parse_args()
    
    # Resolve input path
    input_path = Path(args.input_file)
    if not input_path.is_absolute():
        input_path = PROJECT_ROOT / input_path
    
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    # Run orchestrator
    orchestrator = Orchestrator(verbose=not args.quiet)
    
    if args.output_dir:
        orchestrator.output_dir = Path(args.output_dir)
    
    result = orchestrator.run(str(input_path))
    
    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
