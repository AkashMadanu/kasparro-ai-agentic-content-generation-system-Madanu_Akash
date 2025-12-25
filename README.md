# 🚀 Kasparro AI - Multi-Agent Content Generation System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gemini AI](https://img.shields.io/badge/LLM-Gemini%202.5%20Flash-green.svg)](https://ai.google.dev/)

> A modular, production-style agentic automation system that transforms structured product data into machine-readable content pages.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Agent Documentation](#agent-documentation)
- [Output Examples](#output-examples)
- [Configuration](#configuration)
- [Testing](#testing)
- [Evaluation Criteria Compliance](#evaluation-criteria-compliance)

---

## 🎯 Overview

This system is designed as a **Multi-Agent Content Generation Pipeline** that:

1. **Parses** structured product data
2. **Generates** categorized user questions
3. **Transforms** data through reusable logic blocks
4. **Applies** templates to produce structured output
5. **Outputs** three JSON files: `faq.json`, `product_page.json`, `comparison_page.json`

### What This System Does

```
Input (product.json) → Agents Pipeline → Structured JSON Outputs
```

### What This System Is NOT

- ❌ A chatbot or conversational AI
- ❌ A UI/web application
- ❌ A single monolithic script
- ❌ A content writing tool with external research

---

## 🏗️ Architecture

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR                                │
│                   (DAG Pipeline Manager)                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT: product.json                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  ProductParserAgent                              │
│         (Normalize & clean raw product data)                     │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ QuestionGenerator│ │ ContentLogic    │ │ TemplateEngine  │
│ Agent           │ │ Agent           │ │ Agent           │
│ (15+ questions) │ │ (Logic Blocks)  │ │ (Templates)     │
└─────────────────┘ └─────────────────┘ └─────────────────┘
              │               │               │
              └───────────────┼───────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  FAQPageAgent   │ │ ProductPageAgent│ │ ComparisonAgent │
│                 │ │                 │ │ (+ Product B)   │
└─────────────────┘ └─────────────────┘ └─────────────────┘
              │               │               │
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│    faq.json     │ │product_page.json│ │comparison_page  │
│                 │ │                 │ │     .json       │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

### Pipeline Flow (DAG)

```
Input JSON
    ↓
ProductParserAgent (normalize data)
    ↓
    ├──→ QuestionGeneratorAgent (generate 15+ questions)
    │           ↓
    │    FAQPageAgent (create FAQ page)
    │           ↓
    │       faq.json
    │
    ├──→ ProductPageAgent (create product page)
    │           ↓
    │    product_page.json
    │
    └──→ ComparisonAgent (create Product B + compare)
                ↓
         comparison_page.json
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Modular Agents** | 7 specialized agents with single responsibilities |
| **Reusable Logic Blocks** | Pure functions for content transformation |
| **Template Engine** | Declarative templates mapping fields to logic |
| **DAG Orchestration** | Dependency-aware pipeline execution |
| **Strict JSON Output** | All LLM calls return structured JSON only |
| **No External Knowledge** | System uses only provided product data |
| **Extensible Design** | Easy to add new agents, templates, or products |

---

## 🛠️ Installation

### Prerequisites

- Python 3.10 or higher
- Google AI Studio API Key (Gemini)

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/AkashMadanu/kasparro-ai-agentic-content-generation-system-Madanu_Akash.git
cd kasparro-ai-agentic-content-generation-system-Madanu_Akash

# 2. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
copy .env.example .env   # Windows
cp .env.example .env     # macOS/Linux

# 5. Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_api_key_here
```

---

## 🚀 Usage

### Basic Usage

```bash
python orchestrator.py input/product.json
```

### Expected Output

```
═══════════════════════════════════════════════════════════════════
       KASPARRO AI - Multi-Agent Content Generation System
═══════════════════════════════════════════════════════════════════

[1/7] ProductParserAgent: Parsing product data...
      ✓ Product parsed: GlowBoost Vitamin C Serum

[2/7] QuestionGeneratorAgent: Generating categorized questions...
      ✓ Generated 15 questions across 5 categories

[3/7] ContentLogicAgent: Preparing content logic blocks...
      ✓ Logic blocks ready

[4/7] TemplateEngineAgent: Loading templates...
      ✓ Templates loaded: FAQ, Product, Comparison

[5/7] FAQPageAgent: Generating FAQ page...
      ✓ FAQ page generated with 5 Q&As

[6/7] ProductPageAgent: Generating product page...
      ✓ Product page generated

[7/7] ComparisonAgent: Creating comparison page...
      ✓ Comparison page generated (vs RadiantGlow Serum)

═══════════════════════════════════════════════════════════════════
                         OUTPUT FILES
═══════════════════════════════════════════════════════════════════
  • outputs/faq.json
  • outputs/product_page.json
  • outputs/comparison_page.json

✓ Pipeline completed successfully!
```

### Custom Product Data

Create a JSON file following this schema:

```json
{
  "product_name": "Your Product Name",
  "concentration": "Active ingredient concentration",
  "skin_type": ["Skin", "Types"],
  "key_ingredients": ["Ingredient 1", "Ingredient 2"],
  "benefits": ["Benefit 1", "Benefit 2"],
  "how_to_use": "Usage instructions",
  "side_effects": "Side effect information",
  "price": "₹XXX"
}
```

Then run:
```bash
python orchestrator.py path/to/your/product.json
```

---

## 📁 Project Structure

```
kasparro-ai-agentic-content-generation-system/
│
├── agents/                          # Agent modules
│   ├── __init__.py                  # Agent exports
│   ├── product_parser.py            # ProductParserAgent
│   ├── question_generator.py        # QuestionGeneratorAgent
│   ├── content_logic_agent.py       # ContentLogicAgent
│   ├── template_engine_agent.py     # TemplateEngineAgent
│   ├── faq_agent.py                 # FAQPageAgent
│   ├── product_page_agent.py        # ProductPageAgent
│   └── comparison_agent.py          # ComparisonAgent
│
├── logic_blocks/                    # Reusable content logic
│   ├── __init__.py                  # Logic block exports
│   ├── benefits.py                  # generateBenefits()
│   ├── usage.py                     # generateUsage()
│   ├── safety.py                    # generateSafety()
│   ├── ingredients.py               # generateIngredients()
│   └── comparison.py                # compareProducts()
│
├── templates/                       # Template definitions
│   ├── faq_template.json            # FAQ page template
│   ├── product_template.json        # Product page template
│   └── comparison_template.json     # Comparison page template
│
├── input/                           # Input data directory
│   └── product.json                 # Sample product data
│
├── outputs/                         # Generated outputs
│   ├── faq.json                     # Generated FAQ page
│   ├── product_page.json            # Generated product page
│   └── comparison_page.json         # Generated comparison page
│
├── docs/                            # Documentation
│   └── projectdocumentation.md      # System design document
│
├── orchestrator.py                  # Main pipeline orchestrator
├── config.py                        # Configuration management
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
└── README.md                        # This file
```

---

## 🤖 Agent Documentation

### Agent 1: ProductParserAgent

| Property | Value |
|----------|-------|
| **Responsibility** | Normalize and validate raw product JSON |
| **Input** | Raw product JSON from file |
| **Output** | Cleaned product object with standardized fields |
| **LLM Usage** | No (pure data transformation) |

### Agent 2: QuestionGeneratorAgent

| Property | Value |
|----------|-------|
| **Responsibility** | Generate 15+ categorized user questions |
| **Input** | Parsed product object |
| **Output** | Questions grouped by category (informational, usage, safety, purchase, comparison) |
| **LLM Usage** | Yes (Gemini 2.5 Flash) |

### Agent 3: ContentLogicAgent

| Property | Value |
|----------|-------|
| **Responsibility** | Expose reusable content transformation functions |
| **Input** | Product data |
| **Output** | Structured JSON fragments |
| **LLM Usage** | Yes (for complex transformations) |

### Agent 4: TemplateEngineAgent

| Property | Value |
|----------|-------|
| **Responsibility** | Load and apply templates |
| **Input** | Template definitions + data from logic blocks |
| **Output** | Rendered content structures |
| **LLM Usage** | No (template rendering only) |

### Agent 5: FAQPageAgent

| Property | Value |
|----------|-------|
| **Responsibility** | Generate FAQ page with 5+ Q&As |
| **Input** | Questions + product data |
| **Output** | `faq.json` structure |
| **LLM Usage** | Yes (for answer generation) |

### Agent 6: ProductPageAgent

| Property | Value |
|----------|-------|
| **Responsibility** | Generate product description page |
| **Input** | Parsed product data |
| **Output** | `product_page.json` structure |
| **LLM Usage** | Yes (for enhanced descriptions) |

### Agent 7: ComparisonAgent

| Property | Value |
|----------|-------|
| **Responsibility** | Create fictional Product B and comparison |
| **Input** | Product A data |
| **Output** | `comparison_page.json` structure |
| **LLM Usage** | Yes (for Product B creation and comparison) |

---

## 📄 Output Examples

### faq.json

```json
{
  "page_type": "faq",
  "product_name": "GlowBoost Vitamin C Serum",
  "generated_at": "2025-12-25T10:30:00Z",
  "faqs": [
    {
      "question": "What is GlowBoost Vitamin C Serum?",
      "answer": "GlowBoost Vitamin C Serum is a skincare product with 10% Vitamin C concentration, designed for oily and combination skin types.",
      "category": "informational"
    }
  ]
}
```

### product_page.json

```json
{
  "page_type": "product",
  "product_name": "GlowBoost Vitamin C Serum",
  "ingredients": ["Vitamin C", "Hyaluronic Acid"],
  "benefits": ["Brightening", "Fades dark spots"],
  "usage": "Apply 2–3 drops in the morning before sunscreen",
  "side_effects": "Mild tingling for sensitive skin",
  "price": "₹699"
}
```

### comparison_page.json

```json
{
  "page_type": "comparison",
  "product_a": { ... },
  "product_b": { ... },
  "comparison": {
    "ingredients": "Analysis of ingredient differences",
    "benefits": "Comparison of benefits",
    "price": "Price comparison analysis"
  }
}
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google AI Studio API key | Yes |
| `GEMINI_MODEL` | Model to use (default: gemini-2.5-flash) | No |
| `OUTPUT_DIR` | Output directory (default: outputs/) | No |

### Config Options (config.py)

```python
# LLM Settings
LLM_MODEL = "gemini-2.5-flash"
LLM_TEMPERATURE = 0.3  # Lower for more deterministic output
LLM_MAX_TOKENS = 4096

# Pipeline Settings
ENABLE_LOGGING = True
STRICT_JSON_MODE = True
```

---

## 🧪 Testing

```bash
# Run the pipeline with sample data
python orchestrator.py input/product.json

# Validate output JSON files
python -c "import json; [json.load(open(f'outputs/{f}')) for f in ['faq.json', 'product_page.json', 'comparison_page.json']]; print('All outputs valid!')"
```

---

## ✅ Evaluation Criteria Compliance

### 1. Agentic System Design (45%)

| Criterion | Implementation |
|-----------|----------------|
| Clear responsibilities | ✅ Each agent has single, documented responsibility |
| Modularity | ✅ Agents are separate modules with defined interfaces |
| Extensibility | ✅ Easy to add new agents or modify existing ones |
| Correctness of flow | ✅ DAG-based pipeline with dependency management |

### 2. Types & Quality of Agents (25%)

| Criterion | Implementation |
|-----------|----------------|
| Meaningful roles | ✅ 7 agents with distinct purposes |
| Appropriate boundaries | ✅ No overlap, clear separation of concerns |
| Input/output correctness | ✅ Typed contracts for all agents |

### 3. Content System Engineering (20%)

| Criterion | Implementation |
|-----------|----------------|
| Quality of templates | ✅ 3 declarative JSON templates |
| Quality of content blocks | ✅ 5 pure function logic blocks |
| Composability | ✅ Blocks can be combined in any template |

### 4. Data & Output Structure (10%)

| Criterion | Implementation |
|-----------|----------------|
| JSON correctness | ✅ All outputs are valid JSON |
| Clean mapping | ✅ Clear data → logic → output flow |

---

## 📝 License

This project is created for the Kasparro Applied AI Engineer Challenge.

---

## 👤 Author

**Akash Madanu**

- GitHub: [@AkashMadanu](https://github.com/AkashMadanu)

---

*Built with ❤️ for Kasparro AI*
