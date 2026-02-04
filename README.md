# Document Extraction System

A Python-based document extraction system that processes PDF, DOCX, PPTX, and XLSX files into structured output: clean markdown text, extracted tables (as JSON), image metadata, and document metadata. Designed for GenAI pipelines where extraction quality directly impacts downstream RAG performance.

## Overview

This system serves as the ingestion layer for document processing pipelines. It uses a Strategy pattern to handle multiple file formats through a unified interface, producing consistent `ExtractionResult` objects regardless of input format. The design prioritizes partial success — a corrupt table on page 5 won't prevent extraction of pages 1-4.

## Architecture

```
Input File → DocumentRouter → Format Extractor → ExtractionResult
```

Each file format has its own extractor class implementing a shared abstract interface (`BaseExtractor`). The `DocumentRouter` inspects file extensions and dispatches to the correct extractor. Adding a new format means creating one new class — no existing code changes required.

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### CLI Usage

```bash
# Extract document to JSON (saves to same directory as input)
python -m src report.pdf
# → Creates report_extracted.json

# Specify output file
python -m src report.pdf -o results.json

# Try with included sample
python -m src sample_docs/quarterly_report.pdf

# View help
python -m src --help
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
| PDF    | Full   | Text with heading detection, tables, images, metadata |
| DOCX   | Stub   | Architecture supports it, implementation pending |
| PPTX   | Stub   | Architecture supports it, implementation pending |
| XLSX   | Stub   | Architecture supports it, implementation pending |

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
    ├── .gitkeep
    ├── quarterly_report.pdf
    └── quarterly_report_extracted.json
```

## Design Decisions

- **Strategy Pattern**: Each format gets its own extractor class implementing a shared interface. Adding formats requires no changes to existing code.
- **Pydantic Models**: All data models use Pydantic for validation, serialization, and self-documenting schemas.
- **Partial Success**: `ExtractionResult.errors` captures non-fatal issues so usable content is always returned, even if some elements fail.
- **Markdown Output**: Text is converted to markdown with heading hierarchy preserved — the lingua franca for LLM input and semantic chunking.

See [LIMITATIONS.md](LIMITATIONS.md) for known gaps and future improvements.
