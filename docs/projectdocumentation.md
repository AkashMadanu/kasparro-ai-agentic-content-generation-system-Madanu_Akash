# Project Documentation

## Multi-Agent Content Generation System

---

## 1. Problem Statement

Design and implement a **modular agentic automation system** that takes a small product dataset and automatically generates structured, machine-readable content pages.

### Core Requirements:
- Parse and understand product data
- Automatically generate categorized user questions (15+ minimum)
- Define and implement custom templates
- Create reusable content logic blocks
- Assemble 3 output pages (FAQ, Product, Comparison)
- Output clean, machine-readable JSON
- Pipeline must run via agents (not a single-script GPT wrapper)

### Constraints:
- No external facts beyond input data
- No UI/web application
- No monolithic architecture
- All outputs must be structured JSON

---

## 2. Solution Overview

The solution implements a **7-agent pipeline architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (DAG Pipeline)                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ProductParserAgent                           │
│              (Normalize & validate input data)                   │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌──────────────────────┐          ┌──────────────────────┐
│ QuestionGenerator    │          │ ContentLogicAgent    │
│ Agent                │          │ (Logic Blocks)       │
│ (15+ questions)      │          └──────────────────────┘
└──────────────────────┘                    │
              │                             │
              │     ┌───────────────────────┘
              │     │
              ▼     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TemplateEngineAgent                           │
│              (Template definitions & rendering)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│   FAQPageAgent   │ │ProductPageAgent  │ │ ComparisonAgent  │
└──────────────────┘ └──────────────────┘ └──────────────────┘
              │               │               │
              ▼               ▼               ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│    faq.json      │ │ product_page.json│ │comparison_page   │
│                  │ │                  │ │    .json         │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

### Technology Stack:
- **Language**: Python 3.10+
- **LLM**: Google Gemini 2.5 Flash
- **Architecture Pattern**: DAG (Directed Acyclic Graph) Pipeline
- **Output Format**: JSON

---

## 3. Scopes & Assumptions

### In Scope:
- Single product input processing
- 7-agent modular architecture
- 3 output page types (FAQ, Product, Comparison)
- 5 reusable logic blocks
- 3 template definitions
- LLM-powered content generation (Gemini)
- JSON-only outputs

### Assumptions:
1. Input follows the defined product schema
2. Gemini API is available and rate limits are sufficient
3. All product data is in English
4. Fictional Product B for comparison is acceptable
5. Single-threaded synchronous execution

### Out of Scope:
- Multi-product batch processing
- Database storage
- API endpoints
- User interface
- Real-time processing
- Multi-language support

---

## 4. System Design

### 4.1 Agent Architecture

Each agent follows these principles:
- **Single Responsibility**: One clear purpose
- **Defined Contract**: Explicit input/output schemas
- **Stateless**: No hidden global state
- **Composable**: Can be combined in different pipelines

#### Agent Specifications:

| Agent | Responsibility | Input | Output | LLM |
|-------|---------------|-------|--------|-----|
| ProductParserAgent | Normalize raw product data | Raw JSON | Parsed product object | No |
| QuestionGeneratorAgent | Generate 15+ categorized questions | Parsed product | Categorized questions | Yes |
| ContentLogicAgent | Expose content transformation functions | Product data | JSON fragments | Partial |
| TemplateEngineAgent | Load and validate templates | Template files | Template objects | No |
| FAQPageAgent | Generate FAQ page | Product + Questions | faq.json | Yes |
| ProductPageAgent | Generate product description | Parsed product | product_page.json | Yes |
| ComparisonAgent | Create comparison with fictional product | Parsed product | comparison_page.json | Yes |

### 4.2 Data Flow

```
┌─────────────┐
│ product.json│ (Raw Input)
└──────┬──────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│ ProductParserAgent                                    │
│ ┌──────────────────────────────────────────────────┐ │
│ │ • Load JSON file                                 │ │
│ │ • Validate against input schema                  │ │
│ │ • Normalize field names                          │ │
│ │ • Extract numeric values (price, concentration)  │ │
│ │ • Generate unique product ID                     │ │
│ └──────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
       │
       │ Parsed Product Object
       ▼
┌──────────────────────────────────────────────────────┐
│ QuestionGeneratorAgent                                │
│ ┌──────────────────────────────────────────────────┐ │
│ │ • Build LLM prompt with product data             │ │
│ │ • Call Gemini API (JSON mode)                    │ │
│ │ • Parse response into categories                 │ │
│ │ • Validate minimum question count (15+)          │ │
│ └──────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
       │
       │ Categorized Questions
       ▼
┌──────────────────────────────────────────────────────┐
│ Page Generation Agents (Parallel-Ready)               │
│                                                       │
│ ┌────────────────┐ ┌────────────────┐ ┌────────────┐ │
│ │ FAQPageAgent   │ │ProductPageAgent│ │Comparison  │ │
│ │                │ │                │ │Agent       │ │
│ │ • Select Q's   │ │ • Use logic    │ │            │ │
│ │ • Generate A's │ │   blocks       │ │ • Create   │ │
│ │ • Apply FAQ    │ │ • Enhance via  │ │   Product B│ │
│ │   template     │ │   LLM          │ │ • Compare  │ │
│ │                │ │ • Apply        │ │ • Analyze  │ │
│ │                │ │   template     │ │            │ │
│ └───────┬────────┘ └───────┬────────┘ └─────┬──────┘ │
└─────────┼──────────────────┼────────────────┼────────┘
          │                  │                │
          ▼                  ▼                ▼
    ┌──────────┐      ┌──────────────┐  ┌──────────────┐
    │ faq.json │      │product_page  │  │comparison    │
    │          │      │   .json      │  │ _page.json   │
    └──────────┘      └──────────────┘  └──────────────┘
```

### 4.3 Logic Blocks

Reusable content transformation functions:

```python
# logic_blocks/

generate_benefits(product) → {
    "type": "benefits",
    "items": [...],
    "summary": "..."
}

generate_usage(product) → {
    "type": "usage",
    "steps": [...],
    "tips": [...],
    "frequency": "..."
}

generate_safety(product) → {
    "type": "safety",
    "side_effects": {...},
    "warnings": [...],
    "precautions": [...]
}

generate_ingredients(product) → {
    "type": "ingredients",
    "items": [...],
    "hero_ingredient": "..."
}

compare_products(product_a, product_b) → {
    "type": "comparison",
    "dimensions": {...},
    "scores": {...}
}
```

### 4.4 Template Structure

Templates are declarative JSON definitions that map fields to data sources:

```json
{
    "template_name": "faq",
    "fields": {
        "page_type": {"default": "faq"},
        "product_name": {"source": "product.name"},
        "faqs": {
            "type": "array",
            "item_schema": {
                "question": {"type": "string"},
                "answer": {"type": "string"},
                "category": {"type": "string"}
            }
        }
    },
    "required_blocks": ["safety", "usage", "benefits"]
}
```

### 4.5 LLM Integration

All LLM calls follow these patterns:

1. **System Role**: Each agent has a defined role
2. **JSON Mode**: Gemini configured for JSON-only output
3. **Schema Enforcement**: Output must match expected schema
4. **Data Grounding**: Only provided product data, no external facts

Example prompt structure:
```
You are the [AgentName] in a multi-agent content generation system.

PRODUCT DATA:
[Structured product information]

REQUIREMENTS:
[Specific requirements and constraints]

OUTPUT FORMAT (strict JSON):
[Expected JSON schema]

Generate the content now. Return ONLY valid JSON, no explanations.
```

### 4.6 Error Handling

- **Input Validation**: Schema validation at entry point
- **LLM Response Parsing**: JSON parsing with fallback cleanup
- **Pipeline Errors**: Graceful failure with informative messages
- **Output Validation**: Verify generated outputs meet requirements

---

## 5. Sequence Diagram

```
┌──────────┐    ┌────────┐    ┌─────────┐    ┌──────────┐    ┌─────────┐
│Orchestrator│    │Parser  │    │Question │    │ Page     │    │ Output  │
│          │    │ Agent  │    │ Agent   │    │ Agents   │    │ Files   │
└────┬─────┘    └───┬────┘    └────┬────┘    └────┬─────┘    └────┬────┘
     │              │              │              │              │
     │ load(input)  │              │              │              │
     │─────────────>│              │              │              │
     │              │              │              │              │
     │ parsed_product              │              │              │
     │<─────────────│              │              │              │
     │              │              │              │              │
     │ generate(product)           │              │              │
     │────────────────────────────>│              │              │
     │              │              │              │              │
     │              │    [LLM Call - Gemini]      │              │
     │              │              │──────┐       │              │
     │              │              │<─────┘       │              │
     │              │              │              │              │
     │ questions                   │              │              │
     │<────────────────────────────│              │              │
     │              │              │              │              │
     │ generate_pages(product, questions)         │              │
     │───────────────────────────────────────────>│              │
     │              │              │              │              │
     │              │              │    [LLM Calls]              │
     │              │              │              │──────┐       │
     │              │              │              │<─────┘       │
     │              │              │              │              │
     │ page_jsons                  │              │              │
     │<──────────────────────────────────────────│              │
     │              │              │              │              │
     │ write_outputs()             │              │              │
     │─────────────────────────────────────────────────────────>│
     │              │              │              │              │
     │ success      │              │              │              │
     │<─────────────────────────────────────────────────────────│
     │              │              │              │              │
```

---

## 6. Directory Structure

```
kasparro-ai-agentic-content-generation-system/
│
├── agents/                     # Agent modules
│   ├── __init__.py
│   ├── product_parser.py       # ProductParserAgent
│   ├── question_generator.py   # QuestionGeneratorAgent
│   ├── content_logic_agent.py  # ContentLogicAgent
│   ├── template_engine_agent.py# TemplateEngineAgent
│   ├── faq_agent.py            # FAQPageAgent
│   ├── product_page_agent.py   # ProductPageAgent
│   └── comparison_agent.py     # ComparisonAgent
│
├── logic_blocks/               # Reusable content logic
│   ├── __init__.py
│   ├── benefits.py             # generate_benefits()
│   ├── usage.py                # generate_usage()
│   ├── safety.py               # generate_safety()
│   ├── ingredients.py          # generate_ingredients()
│   └── comparison.py           # compare_products()
│
├── templates/                  # Template definitions
│   ├── faq_template.json
│   ├── product_template.json
│   └── comparison_template.json
│
├── input/                      # Input data
│   └── product.json
│
├── outputs/                    # Generated outputs
│   ├── faq.json
│   ├── product_page.json
│   └── comparison_page.json
│
├── docs/                       # Documentation
│   └── projectdocumentation.md
│
├── orchestrator.py             # Main pipeline orchestrator
├── config.py                   # Configuration
├── requirements.txt            # Dependencies
├── .env.example                # Environment template
└── README.md                   # Project README
```

---

## 7. Configuration

### Environment Variables:
| Variable | Description | Required |
|----------|-------------|----------|
| GEMINI_API_KEY | Google AI Studio API key | Yes |
| GEMINI_MODEL | Model name (default: gemini-1.5-flash) | No |
| OUTPUT_DIR | Output directory path | No |
| DEBUG | Enable debug logging | No |

### LLM Configuration:
```python
LLM_CONFIG = {
    "temperature": 0.3,    # Lower = more deterministic
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 4096
}
```

---

## 8. Extensibility

The system is designed for extension:

### Adding New Agents:
1. Create new file in `agents/`
2. Implement agent class with `generate()` method
3. Register in `agents/__init__.py`
4. Add to orchestrator pipeline

### Adding New Logic Blocks:
1. Create new file in `logic_blocks/`
2. Implement pure function returning JSON fragment
3. Export from `logic_blocks/__init__.py`

### Adding New Templates:
1. Create JSON file in `templates/`
2. Define fields and sources
3. Template auto-loads on startup

### Adding New Product Types:
1. Update `PRODUCT_INPUT_SCHEMA` in config
2. Adjust agent prompts as needed
3. System adapts to new schema

---

*Document Version: 1.0*  
*Last Updated: December 25, 2025*
