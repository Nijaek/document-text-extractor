# Document Extraction System

<!-- TODO: Write 2-3 sentence overview -->
A Python-based document extraction system that processes PDF, DOCX, and PPTX files...

## Overview

<!-- TODO: Expand on what this does and why -->

## Architecture

<!-- TODO: Describe Strategy pattern approach -->

```
Input File → DocumentRouter → Format Extractor → ExtractionResult
```

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### CLI Usage

```bash
# Extract document to JSON (creates report_extracted.json)
python -m src report.pdf

# Specify output file
python -m src report.pdf -o results.json
```

### Library Usage

```python
from src import process_document

result = process_document("path/to/document.pdf")
print(result.markdown)
print(result.tables)
print(result.metadata)
```

## Supported Formats

| Format | Status | Notes |
|--------|--------|-------|
| PDF    | Full   | <!-- TODO: Add notes --> |
| DOCX   | Full   | <!-- TODO: Add notes --> |
| PPTX   | Stub   | Architecture supports it, not yet implemented |
| XLSX   | Stub   | Architecture supports it, not yet implemented |

## Running Tests

```bash
pytest tests/ -v
```

## Project Structure

```
document-extractor/
├── README.md
├── LIMITATIONS.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── __main__.py
│   ├── models.py
│   ├── router.py
│   ├── base_extractor.py
│   ├── logging_config.py
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── pdf_extractor.py
│   │   ├── docx_extractor.py
│   │   ├── pptx_extractor.py
│   │   └── xlsx_extractor.py
│   └── utils/
│       ├── __init__.py
│       └── markdown_helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_router.py
│   ├── test_pdf_extractor.py
│   ├── test_docx_extractor.py
│   ├── test_pptx_extractor.py
│   ├── test_xlsx_extractor.py
│   └── test_utils.py
└── sample_docs/
    └── .gitkeep
```

## Design Decisions

<!-- TODO: Write 1-2 sentences for each -->

- **Strategy Pattern**: ...
- **Pydantic Models**: ...
- **Partial Success**: ...
- **Markdown Output**: ...

See [LIMITATIONS.md](LIMITATIONS.md) for known gaps and future improvements.
