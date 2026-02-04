# Document Extraction System — Claude Code Project Plan

## IMPORTANT: Read This Entire Document Before Writing Any Code

This document is the single source of truth for building this project. Every design decision has been made deliberately. Do not deviate from the architecture, patterns, or structure described here unless you encounter a technical impossibility — and if you do, document what you changed and why.

---

## 1. Project Background

### What Is This?

A Python-based document extraction system that processes PDF, DOCX, and PPTX files and produces structured output: clean markdown text, extracted tables (as JSON), image metadata, and document metadata. The output is unified across all formats via a shared data model.

---

## 2. Design Decisions (Do Not Change These)

### 2.1 Strategy Pattern for Extractors

**Decision:** Each file format gets its own extractor class that implements a shared abstract interface.

**Why:** Different formats have completely different internals (PDF is page-based, DOCX is paragraph-based, PPTX is slide-based), but consumers of the extraction need a uniform output. The Strategy pattern means:
- Adding a new format = one new file implementing the interface
- No existing extractor code is modified (Open/Closed Principle)
- Each extractor is independently testable

### 2.2 Pydantic for Data Models

**Decision:** All data models use Pydantic's `BaseModel`.

**Why:**
- **Validation** — Bad data from an extractor is caught at the model boundary, not downstream
- **Serialization** — `.model_dump()` and `.model_dump_json()` provide API-ready output for free
- **Self-documenting** — A new team member reads the model and understands the contract
- **Type safety** — Works naturally with Python type hints and IDE autocomplete

### 2.3 Partial Success via `errors` Field

**Decision:** `ExtractionResult` includes an `errors: list[str]` field for non-fatal issues.

**Why:** Enterprise documents are messy. A 50-page PDF might have 49 clean pages and one corrupt table. The system should return everything it *can* extract plus transparency about what failed. Throwing an exception and returning nothing is unacceptable in a production pipeline.

### 2.4 Markdown as Primary Text Output

**Decision:** Extracted text is converted to markdown with heading hierarchy preserved.

**Why:** Markdown is the lingua franca for LLM input. Proper heading hierarchy (H1, H2, H3) gives a language model structural understanding of the document. In a RAG pipeline, this means:
- Better semantic chunking (split on headings, not arbitrary character counts)
- Preserved document structure in retrieved context
- Clean formatting without HTML overhead

### 2.5 Tables as Structured JSON (2D Arrays)

**Decision:** Tables are extracted as `list[list[str]]` — a 2D array of cell values.

**Why:** Plain text extraction destroys table relationships. A 2D array preserves row-column structure so an LLM can reason over tabular data. If someone asks "what was Q3 revenue?", the model needs to understand which cells belong to which columns.

### 2.6 Library Selections

| Format | Library | Package Name | Why |
|---|---|---|---|
| PDF | PyMuPDF | `pymupdf` | Fast, handles text + tables + images in one package. PyPDF2 is deprecated. pypdf doesn't handle tables/images natively. |
| DOCX | python-docx | `python-docx` | Standard, well-maintained, handles paragraphs + tables + images |
| PPTX | python-pptx | `python-pptx` | Standard, well-maintained, slide-by-slide extraction |
| XLSX | openpyxl | `openpyxl` | Standard, well-maintained, workbook/sheet-based extraction |
| Models | Pydantic | `pydantic` | Validation, serialization, self-documenting schemas |
| Testing | pytest | `pytest` | Industry standard, clean assertions, fixtures |

**Do NOT use:** LangChain, LlamaIndex, or any high-level framework document loaders. This challenge tests whether the candidate understands extraction fundamentals, not whether they can call someone else's API.

### 2.7 Import Strategy

**Decision:** Use relative imports within the `src` package.

**Why:**
- Absolute imports like `from src.models import ...` only work when running from the project root
- Relative imports (`from .models import ...`) work regardless of where Python is invoked
- This is the standard pattern for internal package imports

**Examples:**

```python
# In src/router.py
from .models import ExtractionResult, FileFormat
from .extractors import PDFExtractor, DOCXExtractor

# In src/extractors/pdf_extractor.py
from ..models import ExtractionResult, TableData, ImageData, DocumentMetadata
from ..utils.markdown_helpers import clean_text, heading_to_markdown
```

**Note:** External usage (from outside the package) still uses the package name:

```python
from src import process_document
```

---

## 3. Project Structure

Create this exact directory structure. Every file listed below must exist.

```
document-extractor/
├── README.md
├── LIMITATIONS.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── src/
│   ├── __init__.py
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

---

## 4. File-by-File Implementation Instructions

### 4.1 `pyproject.toml`

Standard Python project configuration. Use the following:

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "document-extractor"
version = "0.1.0"
description = "A flexible document extraction system for PDF, DOCX, and PPTX files"
requires-python = ">=3.11"
dependencies = [
    "pymupdf>=1.24.0",
    "python-docx>=1.1.0",
    "python-pptx>=0.6.23",
    "openpyxl>=3.1.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

### 4.2 `requirements.txt`

```
pymupdf>=1.24.0
python-docx>=1.1.0
python-pptx>=0.6.23
openpyxl>=3.1.0
pydantic>=2.0.0
pytest>=8.0.0
pytest-cov>=4.0.0
```

### 4.3 `.gitignore`

Standard Python gitignore. Include: `__pycache__/`, `*.pyc`, `.venv/`, `dist/`, `build/`, `*.egg-info/`, `.pytest_cache/`, `.coverage`, `sample_docs/*.pdf`, `sample_docs/*.docx`, `sample_docs/*.pptx` (keep `.gitkeep`).

---

### 4.4 `src/models.py` — Data Models

This is the contract for the entire system. Implement these Pydantic models exactly:

```python
"""
Data models for the document extraction system.

All extractors produce ExtractionResult as their output, ensuring
a uniform interface regardless of input document format.
"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class FileFormat(str, Enum):
    """Supported document formats."""
    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    XLSX = "xlsx"
    UNKNOWN = "unknown"


class TableData(BaseModel):
    """Represents a single extracted table.

    Content is stored as a 2D array (list of rows, each row is a list of cell strings).
    This preserves row-column relationships for downstream processing,
    which is critical for LLM reasoning over tabular data.
    """
    content: list[list[str]] = Field(
        description="2D array of cell values. First row is typically headers."
    )
    page_or_slide: int | None = Field(
        default=None,
        description="Page number (PDF) or slide number (PPTX) where table appears."
    )
    caption: str | None = Field(
        default=None,
        description="Table caption if available in the source document."
    )


class ImageData(BaseModel):
    """Represents a single extracted image and its metadata.

    In v1, only metadata is extracted (no AI-generated descriptions).
    The description field is reserved for future integration with
    a vision model for automatic captioning.
    """
    filename: str = Field(
        description="Generated filename for the extracted image."
    )
    format: str = Field(
        description="Image format (png, jpg, etc.)."
    )
    width: int | None = Field(
        default=None,
        description="Image width in pixels."
    )
    height: int | None = Field(
        default=None,
        description="Image height in pixels."
    )
    alt_text: str | None = Field(
        default=None,
        description="Alt text from the source document, if available."
    )
    description: str | None = Field(
        default=None,
        description="AI-generated description. Reserved for v2."
    )
    page_or_slide: int | None = Field(
        default=None,
        description="Page or slide number where image appears."
    )


class DocumentMetadata(BaseModel):
    """Metadata about the source document itself."""
    title: str | None = None
    author: str | None = None
    created_date: datetime | None = None
    modified_date: datetime | None = None
    page_count: int | None = None
    file_format: FileFormat
    file_size_bytes: int
    source_filename: str


class ExtractionResult(BaseModel):
    """Unified output from any document extractor.

    Designed for partial success — the errors field captures non-fatal
    issues so that usable content is always returned even if some
    elements fail to extract. This is critical in enterprise pipelines
    where a single corrupt table shouldn't prevent processing 49 clean pages.
    """
    markdown: str = Field(
        description="Full document content as clean markdown."
    )
    tables: list[TableData] = Field(
        default_factory=list,
        description="All tables extracted from the document."
    )
    images: list[ImageData] = Field(
        default_factory=list,
        description="Metadata for all images found in the document."
    )
    metadata: DocumentMetadata
    errors: list[str] = Field(
        default_factory=list,
        description="Non-fatal errors encountered during extraction."
    )
```

**Do not modify these models.** The rest of the system depends on this exact contract.

---

### 4.5 `src/base_extractor.py` — Abstract Base Class

This defines the interface that every extractor must implement.

```python
"""
Abstract base class for document extractors.

Every supported file format implements this interface. The Strategy pattern
allows the DocumentRouter to dispatch to the correct extractor without
knowing format-specific details. Adding a new format means creating a
new class that inherits from BaseExtractor — no existing code changes.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from src.models import (
    ExtractionResult,
    DocumentMetadata,
    TableData,
    ImageData,
)


class BaseExtractor(ABC):
    """Abstract base class for all document format extractors.

    Subclasses must implement the four extraction methods.
    The `extract_all()` method orchestrates them into a unified result.
    """

    def __init__(self, file_path: Path) -> None:
        """Initialize extractor with the path to the document.

        Args:
            file_path: Path to the document file. Must exist and be readable.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file path is not a file.
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        if not self.file_path.is_file():
            raise ValueError(f"Path is not a file: {self.file_path}")

    @abstractmethod
    def extract_text(self) -> str:
        """Extract document text content as clean markdown.

        Returns:
            Document content formatted as markdown with heading
            hierarchy preserved.
        """
        ...

    @abstractmethod
    def extract_tables(self) -> list[TableData]:
        """Extract all tables from the document.

        Returns:
            List of TableData objects, each containing a 2D array
            of cell values.
        """
        ...

    @abstractmethod
    def extract_images(self) -> list[ImageData]:
        """Extract metadata for all images in the document.

        Returns:
            List of ImageData objects with available metadata.
        """
        ...

    @abstractmethod
    def extract_metadata(self) -> DocumentMetadata:
        """Extract document-level metadata.

        Returns:
            DocumentMetadata with available fields populated.
        """
        ...

    def extract_all(self) -> ExtractionResult:
        """Run all extraction methods and return unified result.

        Implements partial success — individual extraction failures
        are captured in the errors list rather than raising exceptions.

        Returns:
            ExtractionResult containing all extractable content
            and a list of any non-fatal errors encountered.
        """
        errors: list[str] = []

        # Extract text (critical — if this fails, report but continue)
        try:
            markdown = self.extract_text()
        except Exception as e:
            markdown = ""
            errors.append(f"Text extraction failed: {e}")

        # Extract tables
        try:
            tables = self.extract_tables()
        except Exception as e:
            tables = []
            errors.append(f"Table extraction failed: {e}")

        # Extract images
        try:
            images = self.extract_images()
        except Exception as e:
            images = []
            errors.append(f"Image extraction failed: {e}")

        # Extract metadata (should rarely fail, but protect anyway)
        try:
            metadata = self.extract_metadata()
        except Exception as e:
            # Metadata is required by the model, so build a minimal one
            from src.models import FileFormat
            metadata = DocumentMetadata(
                file_format=FileFormat.UNKNOWN,
                file_size_bytes=self.file_path.stat().st_size,
                source_filename=self.file_path.name,
            )
            errors.append(f"Metadata extraction failed: {e}")

        return ExtractionResult(
            markdown=markdown,
            tables=tables,
            images=images,
            metadata=metadata,
            errors=errors,
        )
```

**Note:** The `extract_all()` method is fully implemented in the base class. Subclasses only need to implement the four abstract methods. This is intentional — the orchestration logic and error handling pattern should be consistent across all formats.

---

### 4.6 `src/router.py` — DocumentRouter

The router's job is simple: take a file path, determine the format, and return the correct extractor instance.

Implementation requirements:
- Accept a `Path` or `str` as input
- Determine format by file extension (not magic bytes — keep it simple for v1, note magic bytes as a future improvement)
- Return an instantiated extractor ready to use
- Raise a clear `ValueError` for unsupported formats
- Use a registry dict mapping `FileFormat` → extractor class for easy extension
- Include a `supported_formats()` class method that returns available formats
- Include a convenience function `process_document(file_path) -> ExtractionResult` that does routing + extraction in one call

Example usage the router should support:

```python
from src.router import DocumentRouter, process_document

# Option A: Get extractor, then call methods
router = DocumentRouter()
extractor = router.get_extractor("path/to/file.pdf")
result = extractor.extract_all()

# Option B: One-liner convenience
result = process_document("path/to/file.pdf")
```

**Error handling for unsupported formats:**

When a user provides a file with an unsupported extension, raise a `ValueError` with a helpful message that:
1. States which extension was provided
2. Lists all supported formats

Example implementation:

```python
def get_extractor(self, file_path: Path | str) -> BaseExtractor:
    file_path = Path(file_path)
    extension = file_path.suffix.lower().lstrip(".")

    try:
        file_format = FileFormat(extension)
    except ValueError:
        supported = ", ".join(f".{fmt.value}" for fmt in FileFormat if fmt != FileFormat.UNKNOWN)
        raise ValueError(
            f"Unsupported file format: '.{extension}'. "
            f"Supported formats: {supported}"
        )

    # ... rest of routing logic
```

This ensures users get actionable feedback when they provide an unsupported file.

---

### 4.7 `src/extractors/pdf_extractor.py` — PDF Extractor

**This is the most important extractor. Invest the most effort here.**

Use `pymupdf` (imported as `fitz`). Implement all four abstract methods:

**`extract_text()`**
- Iterate through all pages
- Extract text blocks using `page.get_text("dict")` or `page.get_text("blocks")` to access structural information
- Detect headings by font size relative to body text:
  - Largest font → `# H1`
  - Second largest → `## H2`
  - Third largest → `### H3`
  - Everything else → body paragraph
- Preserve paragraph breaks (double newline between paragraphs)
- Handle bold and italic text where detectable
- Strip excessive whitespace but preserve intentional line breaks
- Return clean markdown string

**`extract_tables()`**
- Use `page.find_tables()` (pymupdf built-in table detection)
- For each table found, extract cell values into a 2D list
- Handle `None` or empty cells gracefully (replace with empty string)
- Record which page the table was found on
- Return list of `TableData` objects

**`extract_images()`**
- Use `page.get_images(full=True)` to find all images
- For each image, extract:
  - Image dimensions (width, height)
  - Image format (from the xref data)
  - Generate a filename like `image_p{page}_i{index}.{format}`
- Record which page the image was found on
- Return list of `ImageData` objects
- Wrap individual image extraction in try/except — one corrupt image shouldn't break the whole extraction

**`extract_metadata()`**
- Use `doc.metadata` dict from pymupdf
- Map to `DocumentMetadata` fields: title, author, creation date, modification date
- Page count from `len(doc)`
- File size from `Path.stat().st_size`
- Parse dates from PDF date format (often `D:YYYYMMDDHHmmSS`) — wrap in try/except, return None on failure

**Important edge cases to handle:**
- Empty pages (skip gracefully)
- Pages with only images and no text
- Documents with no tables (return empty list, not an error)
- Encrypted/password-protected PDFs (catch early, add to errors list)

---

### 4.8 `src/extractors/docx_extractor.py` — DOCX Extractor

Use `python-docx`. Implement all four abstract methods:

**`extract_text()`**
- Load document with `Document(file_path)`
- Iterate through `doc.paragraphs`
- Map paragraph styles to markdown headings:
  - `Heading 1` → `# `
  - `Heading 2` → `## `
  - `Heading 3` → `### `
  - `Heading 4` → `#### `
  - `Title` → `# `
  - `List Bullet` / `List Number` → `- ` / `1. `
  - Everything else → body text
- Handle bold (`**text**`) and italic (`*text*`) via run-level formatting
- Skip empty paragraphs but preserve one blank line between blocks
- Return clean markdown string

**`extract_tables()`**
- Iterate through `doc.tables`
- For each table, extract cell text into a 2D list via `row.cells`
- Handle merged cells (python-docx may return duplicate references — deduplicate)
- DOCX doesn't have page numbers easily accessible — set `page_or_slide` to None
- Return list of `TableData` objects

**`extract_images()`**
- Access images through `doc.part.rels` — look for relationship targets with image content types
- For each image relationship:
  - Get the image blob
  - Determine format from content type
  - Get dimensions if available from the corresponding inline shape
  - Generate filename like `image_{index}.{format}`
- Return list of `ImageData` objects

**`extract_metadata()`**
- Use `doc.core_properties` for title, author, created, modified
- Page count is not directly available in python-docx — set to None, note this as a known limitation
- File size from `Path.stat().st_size`
- Return `DocumentMetadata`

---

### 4.9 `src/extractors/pptx_extractor.py` — PPTX Extractor (Stub)

**This extractor should be a documented stub, not a full implementation.** This is a deliberate scoping decision.

Create the class inheriting from `BaseExtractor`. For each method:
- Add a complete docstring explaining what the method *would* do
- Raise `NotImplementedError` with a descriptive message
- Include inline comments explaining the `python-pptx` approach you'd take

Example pattern:

```python
def extract_text(self) -> str:
    """Extract text from all slides as markdown.

    Implementation approach:
    - Iterate through presentation.slides
    - For each slide, iterate through slide.shapes
    - For text frames (shape.has_text_frame), extract paragraphs
    - Map slide titles to H2 headings
    - Preserve bullet/numbered list formatting
    - Separate slides with horizontal rules (---)
    """
    raise NotImplementedError(
        "PPTX text extraction not yet implemented. "
        "Architecture supports it — follows same BaseExtractor pattern. "
        "Estimated implementation time: ~30 minutes."
    )
```

Override `extract_all()` to return a result with empty content and a single error noting the extractor is not yet implemented, rather than raising an exception. This way the router still works end-to-end even for PPTX files.

---

### 4.10 `src/extractors/xlsx_extractor.py` — XLSX Extractor (Stub)

**This extractor should be a documented stub, not a full implementation.** Same approach as PPTX.

Excel files are workbook-based with multiple sheets, each containing cells. This is different from page/paragraph/slide-based formats.

Create the class inheriting from `BaseExtractor`. For each method:
- Add a complete docstring explaining what the method *would* do
- Raise `NotImplementedError` with a descriptive message
- Include inline comments explaining the `openpyxl` approach you'd take

Example pattern:

```python
def extract_text(self) -> str:
    """Extract text from all sheets as markdown.

    Implementation approach:
    - Load workbook with openpyxl.load_workbook(file_path)
    - Iterate through workbook.sheetnames
    - For each sheet, iterate through rows
    - Convert cell values to strings
    - Use sheet names as H2 headings
    - Separate sheets with horizontal rules (---)
    """
    raise NotImplementedError(
        "XLSX text extraction not yet implemented. "
        "Architecture supports it — follows same BaseExtractor pattern. "
        "Estimated implementation time: ~30 minutes."
    )
```

**`extract_tables()` approach:**
- Each sheet is essentially a table
- Could treat each sheet as a TableData with the sheet name as caption
- Or detect distinct table regions within sheets

**`extract_images()` approach:**
- Access images via worksheet._images
- Extract dimensions and format from image objects

**`extract_metadata()` approach:**
- Use workbook.properties for title, author, created, modified
- Sheet count from len(workbook.sheetnames)

Override `extract_all()` to return a result with empty content and a single error noting the extractor is not yet implemented, rather than raising an exception.

---

### 4.11 `src/utils/markdown_helpers.py` — Utility Functions

Create shared utility functions used across extractors:

- `clean_text(text: str) -> str` — Strip excessive whitespace, normalize line endings, remove null characters
- `heading_to_markdown(text: str, level: int) -> str` — Convert text to markdown heading (e.g., `## My Heading`)
- `bold(text: str) -> str` — Wrap in `**`
- `italic(text: str) -> str` — Wrap in `*`
- `table_to_json(table: TableData) -> dict` — Convert TableData to a dict with `headers` and `rows` keys for cleaner JSON output
- `normalize_whitespace(text: str) -> str` — Collapse multiple blank lines to max two

Every function should have a docstring and type hints.

---

### 4.12 `src/extractors/__init__.py`

Export all extractor classes:

```python
from src.extractors.pdf_extractor import PDFExtractor
from src.extractors.docx_extractor import DOCXExtractor
from src.extractors.pptx_extractor import PPTXExtractor
from src.extractors.xlsx_extractor import XLSXExtractor

__all__ = ["PDFExtractor", "DOCXExtractor", "PPTXExtractor", "XLSXExtractor"]
```

### 4.13 `src/__init__.py`

Export the main public interface:

```python
from src.router import DocumentRouter, process_document
from src.models import ExtractionResult, FileFormat

__all__ = ["DocumentRouter", "process_document", "ExtractionResult", "FileFormat"]
```

---

### 4.14 `src/__main__.py` — CLI Entry Point

This enables running the extractor as a module: `python -m src <file>`.

**Usage:**
```bash
# Creates report_extracted.json in current directory
python -m src report.pdf

# Specify output file
python -m src report.pdf -o results.json
```

**Implementation:**
```python
"""
CLI entry point for document extraction.

Usage:
    python -m src <input_file> [-o <output_file>]
"""

import argparse
import sys
from pathlib import Path

from .router import DocumentRouter


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract text, tables, and images from documents."
    )
    parser.add_argument("input_file", type=Path, help="Document to process")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output JSON file (default: <input>_extracted.json)"
    )
    args = parser.parse_args()

    # Validate input file exists
    if not args.input_file.exists():
        print(f"Error: File not found: {args.input_file}", file=sys.stderr)
        return 1

    # Determine output path
    output_path = args.output or args.input_file.with_name(
        f"{args.input_file.stem}_extracted.json"
    )

    # Process document
    router = DocumentRouter()
    try:
        result = router.process_document(args.input_file)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Write output
    output_path.write_text(result.model_dump_json(indent=2))
    print(f"Extracted to: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

### 4.15 Tests — `tests/`

#### `tests/conftest.py`

Create pytest fixtures:
- `tmp_pdf` — Generate a simple PDF using pymupdf with: a title, two paragraphs, a simple 3x3 table, and an embedded image (can be a tiny 1x1 pixel PNG). Return the file path.
- `tmp_docx` — Generate a simple DOCX using python-docx with: a Heading 1, a Heading 2, body paragraphs, a 2x3 table. Return the file path.
- `tmp_pptx` — Generate a minimal PPTX file using python-pptx with one slide containing a title. Return the file path. This is needed to instantiate the extractor even though extraction isn't implemented.
- `tmp_xlsx` — Generate a minimal XLSX file using openpyxl with one sheet containing a few cells. Return the file path. This is needed to instantiate the extractor even though extraction isn't implemented.
- `tmp_empty_pdf` — Generate a PDF with no content (edge case).
- `sample_dir` — Return a `tmp_path` directory for test outputs.

#### `tests/test_models.py`

Test the Pydantic models:
- Test `ExtractionResult` can be created with minimal required fields
- Test `ExtractionResult` serializes to JSON correctly via `.model_dump_json()`
- Test `TableData` accepts a 2D list correctly
- Test `FileFormat` enum values
- Test validation catches bad types (e.g., passing an int where str is expected)

#### `tests/test_router.py`

Test the DocumentRouter:
- Test it returns `PDFExtractor` for `.pdf` files
- Test it returns `DOCXExtractor` for `.docx` files
- Test it raises `ValueError` for unsupported extensions (e.g., `.xyz`)
- Test it raises `FileNotFoundError` for non-existent files
- Test `supported_formats()` returns expected format list
- Test `process_document()` convenience function works end-to-end with a test PDF
- Test unsupported format error message contains the invalid extension
- Test unsupported format error message lists supported formats

Example test for helpful error messages:

```python
def test_unsupported_format_error_message_is_helpful(tmp_path):
    unsupported_file = tmp_path / "document.xyz"
    unsupported_file.touch()

    router = DocumentRouter()
    with pytest.raises(ValueError) as exc_info:
        router.get_extractor(unsupported_file)

    error_message = str(exc_info.value)
    assert ".xyz" in error_message
    assert ".pdf" in error_message
    assert ".docx" in error_message
```

#### `tests/test_pdf_extractor.py`

Test the PDF extractor:
- Test `extract_text()` returns non-empty markdown from the test PDF
- Test `extract_text()` contains expected heading markdown (`# `)
- Test `extract_tables()` returns the expected number of tables
- Test `extract_tables()` first table has correct dimensions
- Test `extract_images()` returns image metadata
- Test `extract_metadata()` returns correct page count
- Test `extract_all()` returns a valid `ExtractionResult`
- Test `extract_all()` on an empty PDF returns empty content with no errors (not an exception)

#### `tests/test_docx_extractor.py`

Test the DOCX extractor:
- Test `extract_text()` returns markdown with heading indicators
- Test `extract_tables()` finds the test table
- Test `extract_metadata()` returns correct format
- Test `extract_all()` returns valid `ExtractionResult`

#### `tests/test_pptx_extractor.py`

Test the PPTX stub extractor:
- Test `PPTXExtractor` can be instantiated with a valid file path
- Test `extract_text()` raises `NotImplementedError` with descriptive message
- Test `extract_tables()` raises `NotImplementedError` with descriptive message
- Test `extract_images()` raises `NotImplementedError` with descriptive message
- Test `extract_metadata()` raises `NotImplementedError` with descriptive message
- Test `extract_all()` returns a valid `ExtractionResult` (not an exception)
- Test `extract_all()` result has an error message indicating PPTX is not implemented
- Test `extract_all()` result has empty markdown, tables, and images lists

Example tests:

```python
import pytest
from src.extractors import PPTXExtractor

def test_pptx_extract_text_raises_not_implemented(tmp_pptx):
    extractor = PPTXExtractor(tmp_pptx)
    with pytest.raises(NotImplementedError) as exc_info:
        extractor.extract_text()
    assert "not yet implemented" in str(exc_info.value).lower()

def test_pptx_extract_all_returns_result_with_error(tmp_pptx):
    extractor = PPTXExtractor(tmp_pptx)
    result = extractor.extract_all()

    assert result.markdown == ""
    assert result.tables == []
    assert result.images == []
    assert len(result.errors) > 0
    assert "pptx" in result.errors[0].lower()
```

#### `tests/test_xlsx_extractor.py`

Test the XLSX stub extractor (same pattern as PPTX):
- Test `XLSXExtractor` can be instantiated with a valid file path
- Test `extract_text()` raises `NotImplementedError` with descriptive message
- Test `extract_tables()` raises `NotImplementedError` with descriptive message
- Test `extract_images()` raises `NotImplementedError` with descriptive message
- Test `extract_metadata()` raises `NotImplementedError` with descriptive message
- Test `extract_all()` returns a valid `ExtractionResult` (not an exception)
- Test `extract_all()` result has an error message indicating XLSX is not implemented
- Test `extract_all()` result has empty markdown, tables, and images lists

#### `tests/test_utils.py`

Test utility functions:
- Test `clean_text()` strips whitespace properly
- Test `heading_to_markdown()` produces correct output for levels 1-4
- Test `normalize_whitespace()` collapses multiple blank lines

---

### 4.16 `README.md`

Write a professional README with these sections:

**Document Extraction System** (title)

**Overview** — 2-3 sentences on what this does and why.

**Architecture** — Brief description of the strategy pattern approach with the ASCII diagram:

```
Input File → DocumentRouter → Format Extractor → ExtractionResult
```

**Quick Start** — Installation and basic usage:

```bash
pip install -r requirements.txt
```

```python
from src import process_document

result = process_document("path/to/document.pdf")
print(result.markdown)
print(result.tables)
print(result.metadata)
```

**Supported Formats** — Table showing PDF (full), DOCX (full), PPTX (stub).

**Running Tests**

```bash
pytest tests/ -v
```

**Project Structure** — The directory tree from section 3.

**Design Decisions** — Brief bullets on Strategy pattern, Pydantic, partial success, markdown output. Keep each to 1-2 sentences.

Link to `LIMITATIONS.md` for known gaps.

---

### 4.17 `LIMITATIONS.md`

Write this as a professional engineering document, not an apology. Frame every limitation with: what it is, why it matters, and how you'd fix it.

Include these items:

| Limitation | Impact | Proposed Solution |
|---|---|---|
| No OCR for scanned/image-only PDFs | Cannot extract text from non-digital PDFs | Integrate Tesseract for local OCR or AWS Textract/Google Document AI for cloud-based OCR |
| PPTX extractor not implemented | Cannot process PowerPoint files | Architecture fully supports it. Implementation follows identical pattern to DOCX extractor. Estimated: 30 minutes |
| No AI-powered image descriptions | Only metadata extracted, no semantic content | Integrate a vision model (Claude, GPT-4V) for automatic captioning. Requires API key management and cost considerations |
| Complex/merged table cells | May produce incorrect cell alignment in some PDFs | Evaluate Camelot or table-detection ML models for higher accuracy on complex layouts |
| No password-protected file support | Encrypted documents fail immediately | Add password parameter to extractors, use pymupdf's decryption for PDF, python-docx doesn't support this natively |
| No streaming for large documents | Memory issues possible on very large files | Implement page-by-page generator pattern to control memory footprint |
| No multi-language support testing | Character encoding issues possible on non-English docs | Add chardet for encoding detection, test against multilingual document corpus |
| Format detection by extension only | Misnamed files would route to wrong extractor | Add python-magic or file signature detection as fallback |
| DOCX page count unavailable | Metadata is incomplete for DOCX files | Would require rendering the document or using an alternative library |

Include a "Future Enhancements" section with:
- CLI interface (`python -m document_extractor path/to/file.pdf`)
- FastAPI wrapper for HTTP API usage
- Batch processing with async support
- Output to file (write markdown, save images to directory)
- Confidence scoring on extraction quality

---

### 4.18 `src/logging_config.py` — Logging Setup

Create a centralized logging configuration:

```python
"""
Logging configuration for the document extraction system.

Usage in any module:
    from .logging_config import get_logger
    logger = get_logger(__name__)
"""

import logging
import sys

# Default format: timestamp, level, module, message
DEFAULT_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DEFAULT_LEVEL = logging.INFO


def get_logger(name: str, level: int = DEFAULT_LEVEL) -> logging.Logger:
    """Get a configured logger for the given module name.

    Args:
        name: Module name, typically __name__
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(DEFAULT_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(level)

    return logger
```

**Usage in extractors:**

```python
from .logging_config import get_logger

logger = get_logger(__name__)

class PDFExtractor(BaseExtractor):
    def extract_text(self) -> str:
        logger.info(f"Extracting text from {self.file_path}")
        # ...
        logger.debug(f"Found {len(blocks)} text blocks on page {page_num}")
        # ...
        logger.warning(f"Page {page_num} contains no extractable text")
```

**Log levels to use:**
- `DEBUG` — Detailed internal state (block counts, parsing steps)
- `INFO` — High-level operations (starting extraction, file loaded)
- `WARNING` — Non-fatal issues (empty page, missing metadata field)
- `ERROR` — Failures captured in the errors list

---

## 5. Implementation Order

Follow this exact sequence. Each step should result in passing tests before moving to the next.

1. **Models** (`src/models.py`) → run `test_models.py`
2. **Utilities** (`src/utils/markdown_helpers.py`) → run `test_utils.py`
3. **Base extractor** (`src/base_extractor.py`) — no tests needed, it's abstract
4. **PDF extractor** (`src/extractors/pdf_extractor.py`) + test fixtures in `conftest.py` → run `test_pdf_extractor.py`
5. **DOCX extractor** (`src/extractors/docx_extractor.py`) → run `test_docx_extractor.py`
6. **PPTX stub** (`src/extractors/pptx_extractor.py`) + fixture in `conftest.py` → run `test_pptx_extractor.py`
7. **XLSX stub** (`src/extractors/xlsx_extractor.py`) + fixture in `conftest.py` → run `test_xlsx_extractor.py`
8. **Router** (`src/router.py`) → run `test_router.py`
9. **Package init files** (`src/__init__.py`, `src/extractors/__init__.py`)
10. **CLI** (`src/__main__.py`) — enables `python -m src <file>`
11. **README.md** and **LIMITATIONS.md**
12. **Full test suite** — `pytest tests/ -v` should pass clean

---

## 6. Code Quality Standards

Apply these throughout every file:

- **Type hints on every function signature** — parameters and return types
- **Docstrings on every public method and class** — Google style preferred
- **No bare except clauses** — always catch specific exceptions
- **No hardcoded paths** — everything uses `Path` objects
- **No print statements** — use `logging` if you need debug output (configure a logger in each module)
- **Constants in UPPER_CASE** at module level if needed
- **Private methods prefixed with underscore** — e.g., `_parse_pdf_date()`
- **Imports organized** — standard library, then third-party, then local, with blank lines between groups

---

## 7. Final Verification Checklist

Before considering this done, verify:

- [ ] `pytest tests/ -v` — all tests pass
- [ ] Every public class and method has a docstring
- [ ] Every function has type hints
- [ ] `README.md` has runnable code examples
- [ ] `LIMITATIONS.md` is complete and honest
- [ ] PPTX stub is documented, not empty
- [ ] `ExtractionResult.errors` is used correctly (non-fatal issues captured, not raised)
- [ ] No bare except clauses anywhere
- [ ] No unused imports
- [ ] Project runs clean from a fresh `pip install -r requirements.txt`
