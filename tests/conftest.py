"""
Pytest fixtures for document extraction tests.

These fixtures generate temporary test documents for use in tests.
"""

import pytest

# TODO: Uncomment when implementing
# import fitz  # pymupdf
# from docx import Document
# from pptx import Presentation


@pytest.fixture
def tmp_pdf(tmp_path):
    """Generate a simple PDF for testing.

    Creates a PDF with:
    - A title (large font)
    - Two body paragraphs
    - A simple 3x3 table
    - An embedded image (tiny 1x1 pixel PNG)

    Returns:
        Path to the generated PDF file.

    Implementation notes:
    - Use fitz.open() to create new PDF
    - Add page with doc.new_page()
    - Insert text with page.insert_text() at different font sizes
    - Create table using page.insert_text() or drawing
    - Embed small PNG image
    - Save to tmp_path / "test.pdf"
    """
    # TODO: Implement PDF fixture
    pass


@pytest.fixture
def tmp_docx(tmp_path):
    """Generate a simple DOCX for testing.

    Creates a DOCX with:
    - A Heading 1
    - A Heading 2
    - Body paragraphs
    - A 2x3 table

    Returns:
        Path to the generated DOCX file.

    Implementation notes:
    - Use Document() to create new document
    - doc.add_heading("Title", level=1)
    - doc.add_paragraph("Body text")
    - doc.add_table(rows=2, cols=3)
    - Save to tmp_path / "test.docx"
    """
    # TODO: Implement DOCX fixture
    pass


@pytest.fixture
def tmp_pptx(tmp_path):
    """Generate a minimal PPTX for testing.

    Creates a PPTX with one slide containing a title.
    Needed to instantiate PPTXExtractor even though extraction
    isn't implemented.

    Returns:
        Path to the generated PPTX file.

    Implementation notes:
    - Use Presentation() to create new presentation
    - Add slide with title layout
    - Set title text
    - Save to tmp_path / "test.pptx"
    """
    # TODO: Implement PPTX fixture
    pass


@pytest.fixture
def tmp_empty_pdf(tmp_path):
    """Generate an empty PDF for edge case testing.

    Creates a PDF with no content (just a blank page).

    Returns:
        Path to the generated PDF file.

    Implementation notes:
    - Use fitz.open() to create new PDF
    - Add single blank page
    - Save to tmp_path / "empty.pdf"
    """
    # TODO: Implement empty PDF fixture
    pass


@pytest.fixture
def sample_dir(tmp_path):
    """Return a temporary directory for test outputs.

    Returns:
        Path to temporary directory.
    """
    # TODO: Return tmp_path or create subdirectory
    pass
