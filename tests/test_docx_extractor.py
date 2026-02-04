"""
Tests for DOCX extractor.
"""

import pytest

from src.extractors import DOCXExtractor
from src.models import ExtractionResult, FileFormat


class TestDOCXExtractorInit:
    """Tests for DOCXExtractor initialization."""

    def test_accepts_valid_docx(self, tmp_docx):
        """Test extractor accepts valid DOCX path."""
        extractor = DOCXExtractor(tmp_docx)
        assert extractor.file_path == tmp_docx


class TestDOCXExtractText:
    """Tests for DOCX text extraction."""

    def test_returns_markdown_with_headings(self, tmp_docx):
        """Test extract_text returns markdown with heading syntax."""
        extractor = DOCXExtractor(tmp_docx)
        result = extractor.extract_text()
        # tmp_docx has Heading 1 and Heading 2
        assert "# " in result

    def test_preserves_paragraph_structure(self, tmp_docx):
        """Test extract_text preserves paragraph breaks."""
        extractor = DOCXExtractor(tmp_docx)
        result = extractor.extract_text()
        # Paragraphs should be separated by double newlines
        assert "\n\n" in result

    def test_contains_expected_content(self, tmp_docx):
        """Test extract_text contains the document content."""
        extractor = DOCXExtractor(tmp_docx)
        result = extractor.extract_text()
        assert "Test Document Title" in result
        assert "Section One" in result


class TestDOCXExtractTables:
    """Tests for DOCX table extraction."""

    def test_finds_tables(self, tmp_docx):
        """Test extract_tables finds the test table."""
        extractor = DOCXExtractor(tmp_docx)
        tables = extractor.extract_tables()
        assert len(tables) >= 1

    def test_table_dimensions(self, tmp_docx):
        """Test extracted table has correct dimensions."""
        extractor = DOCXExtractor(tmp_docx)
        tables = extractor.extract_tables()
        # tmp_docx has a 2x3 table
        assert len(tables[0].content) == 2  # 2 rows
        assert len(tables[0].content[0]) == 3  # 3 columns

    def test_table_content(self, tmp_docx):
        """Test table contains expected cell values."""
        extractor = DOCXExtractor(tmp_docx)
        tables = extractor.extract_tables()
        # Check header row
        assert tables[0].content[0] == ["Header1", "Header2", "Header3"]
        # Check data row
        assert tables[0].content[1] == ["Data1", "Data2", "Data3"]


class TestDOCXExtractMetadata:
    """Tests for DOCX metadata extraction."""

    def test_correct_file_format(self, tmp_docx):
        """Test metadata has correct file format."""
        extractor = DOCXExtractor(tmp_docx)
        metadata = extractor.extract_metadata()
        assert metadata.file_format == FileFormat.DOCX

    def test_page_count_is_none(self, tmp_docx):
        """Test page_count is None (known limitation)."""
        extractor = DOCXExtractor(tmp_docx)
        metadata = extractor.extract_metadata()
        assert metadata.page_count is None

    def test_has_source_filename(self, tmp_docx):
        """Test metadata has source filename."""
        extractor = DOCXExtractor(tmp_docx)
        metadata = extractor.extract_metadata()
        assert metadata.source_filename == "test.docx"

    def test_has_file_size(self, tmp_docx):
        """Test metadata has file size."""
        extractor = DOCXExtractor(tmp_docx)
        metadata = extractor.extract_metadata()
        assert metadata.file_size_bytes > 0


class TestDOCXExtractAll:
    """Tests for DOCX full extraction."""

    def test_returns_valid_result(self, tmp_docx):
        """Test extract_all returns valid ExtractionResult."""
        extractor = DOCXExtractor(tmp_docx)
        result = extractor.extract_all()
        assert isinstance(result, ExtractionResult)
        assert result.markdown != ""

    def test_result_has_tables(self, tmp_docx):
        """Test extract_all result includes tables."""
        extractor = DOCXExtractor(tmp_docx)
        result = extractor.extract_all()
        assert len(result.tables) >= 1

    def test_result_has_no_errors(self, tmp_docx):
        """Test extract_all completes without errors."""
        extractor = DOCXExtractor(tmp_docx)
        result = extractor.extract_all()
        assert result.errors == []
