"""
Tests for PDF extractor.
"""

import pytest

from src.extractors.pdf_extractor import PDFExtractor
from src.models import ExtractionResult, DocumentMetadata, FileFormat


class TestPDFExtractorInit:
    """Tests for PDFExtractor initialization."""

    def test_accepts_valid_pdf(self, tmp_pdf):
        """Test extractor accepts valid PDF path."""
        extractor = PDFExtractor(tmp_pdf)
        assert extractor.file_path == tmp_pdf

    def test_raises_for_missing_file(self, tmp_path):
        """Test extractor raises FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError):
            PDFExtractor(tmp_path / "nonexistent.pdf")


class TestPDFExtractText:
    """Tests for PDF text extraction."""

    def test_returns_non_empty_markdown(self, tmp_pdf):
        """Test extract_text returns non-empty string."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_text()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_contains_heading_markdown(self, tmp_pdf):
        """Test extract_text preserves heading hierarchy."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_text()
        assert "# " in result  # Should have heading syntax

    def test_contains_document_title(self, tmp_pdf):
        """Test extract_text includes document title."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_text()
        assert "Test Document Title" in result

    def test_empty_pdf_returns_empty_string(self, tmp_empty_pdf):
        """Test extract_text returns empty string for empty PDF."""
        extractor = PDFExtractor(tmp_empty_pdf)
        result = extractor.extract_text()
        assert result == ""


class TestPDFExtractTables:
    """Tests for PDF table extraction."""

    def test_returns_list_of_tables(self, tmp_pdf):
        """Test extract_tables returns list."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_tables()
        assert isinstance(result, list)

    def test_table_has_correct_structure(self, tmp_pdf):
        """Test extracted table has 2D array structure."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_tables()
        if len(result) > 0:
            table = result[0]
            assert hasattr(table, 'content')
            assert isinstance(table.content, list)
            if len(table.content) > 0:
                assert isinstance(table.content[0], list)

    def test_records_page_number(self, tmp_pdf):
        """Test extracted table records page number."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_tables()
        if len(result) > 0:
            assert result[0].page_or_slide is not None
            assert result[0].page_or_slide >= 1

    def test_empty_pdf_returns_empty_list(self, tmp_empty_pdf):
        """Test extract_tables returns empty list for empty PDF."""
        extractor = PDFExtractor(tmp_empty_pdf)
        result = extractor.extract_tables()
        assert result == []


class TestPDFExtractImages:
    """Tests for PDF image extraction."""

    def test_returns_list_of_images(self, tmp_pdf):
        """Test extract_images returns list."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_images()
        assert isinstance(result, list)

    def test_image_has_filename(self, tmp_pdf):
        """Test extracted image has generated filename."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_images()
        if len(result) > 0:
            assert result[0].filename is not None
            assert len(result[0].filename) > 0

    def test_image_filename_format(self, tmp_pdf):
        """Test image filename follows expected format."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_images()
        if len(result) > 0:
            # Should be like "image_p1_i0.png"
            assert result[0].filename.startswith("image_p")

    def test_empty_pdf_returns_empty_list(self, tmp_empty_pdf):
        """Test extract_images returns empty list for empty PDF."""
        extractor = PDFExtractor(tmp_empty_pdf)
        result = extractor.extract_images()
        assert result == []


class TestPDFExtractMetadata:
    """Tests for PDF metadata extraction."""

    def test_returns_document_metadata(self, tmp_pdf):
        """Test extract_metadata returns DocumentMetadata."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_metadata()
        assert isinstance(result, DocumentMetadata)

    def test_correct_page_count(self, tmp_pdf):
        """Test metadata has correct page count."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_metadata()
        assert result.page_count == 1

    def test_correct_file_format(self, tmp_pdf):
        """Test metadata has correct file format."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_metadata()
        assert result.file_format == FileFormat.PDF

    def test_has_file_size(self, tmp_pdf):
        """Test metadata has file size."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_metadata()
        assert result.file_size_bytes > 0

    def test_has_source_filename(self, tmp_pdf):
        """Test metadata has source filename."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_metadata()
        assert result.source_filename == "test.pdf"


class TestPDFExtractAll:
    """Tests for PDF full extraction."""

    def test_returns_extraction_result(self, tmp_pdf):
        """Test extract_all returns ExtractionResult."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_all()
        assert isinstance(result, ExtractionResult)

    def test_result_has_markdown(self, tmp_pdf):
        """Test extract_all result has markdown content."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_all()
        assert isinstance(result.markdown, str)
        assert len(result.markdown) > 0

    def test_result_has_metadata(self, tmp_pdf):
        """Test extract_all result has metadata."""
        extractor = PDFExtractor(tmp_pdf)
        result = extractor.extract_all()
        assert result.metadata is not None
        assert result.metadata.file_format == FileFormat.PDF

    def test_empty_pdf_returns_result_not_exception(self, tmp_empty_pdf):
        """Test extract_all on empty PDF returns result with no errors."""
        extractor = PDFExtractor(tmp_empty_pdf)
        result = extractor.extract_all()
        assert isinstance(result, ExtractionResult)
        # Empty PDF is valid, should have no extraction errors
        assert result.markdown == ""
