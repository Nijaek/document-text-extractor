"""
Tests for Pydantic data models.
"""

import json
import pytest
from pydantic import ValidationError

from src.models import (
    FileFormat,
    TableData,
    ImageData,
    DocumentMetadata,
    ExtractionResult,
)


class TestFileFormat:
    """Tests for FileFormat enum."""

    def test_pdf_value(self):
        """Test FileFormat.PDF has correct value."""
        assert FileFormat.PDF.value == "pdf"

    def test_docx_value(self):
        """Test FileFormat.DOCX has correct value."""
        assert FileFormat.DOCX.value == "docx"

    def test_pptx_value(self):
        """Test FileFormat.PPTX has correct value."""
        assert FileFormat.PPTX.value == "pptx"

    def test_xlsx_value(self):
        """Test FileFormat.XLSX has correct value."""
        assert FileFormat.XLSX.value == "xlsx"

    def test_unknown_value(self):
        """Test FileFormat.UNKNOWN has correct value."""
        assert FileFormat.UNKNOWN.value == "unknown"


class TestTableData:
    """Tests for TableData model."""

    def test_create_with_content(self):
        """Test TableData creation with 2D content array."""
        table = TableData(content=[["a", "b"], ["c", "d"]])
        assert table.content == [["a", "b"], ["c", "d"]]

    def test_optional_fields_default_none(self):
        """Test optional fields default to None."""
        table = TableData(content=[["x"]])
        assert table.page_or_slide is None
        assert table.caption is None


class TestImageData:
    """Tests for ImageData model."""

    def test_create_with_required_fields(self):
        """Test ImageData creation with required fields."""
        image = ImageData(filename="test.png", format="png")
        assert image.filename == "test.png"
        assert image.format == "png"

    def test_optional_fields_default_none(self):
        """Test optional fields default to None."""
        image = ImageData(filename="test.png", format="png")
        assert image.width is None
        assert image.height is None
        assert image.alt_text is None
        assert image.description is None
        assert image.page_or_slide is None


class TestDocumentMetadata:
    """Tests for DocumentMetadata model."""

    def test_create_with_required_fields(self):
        """Test DocumentMetadata creation with required fields."""
        metadata = DocumentMetadata(
            file_format=FileFormat.PDF,
            file_size_bytes=1024,
            source_filename="test.pdf"
        )
        assert metadata.file_format == FileFormat.PDF
        assert metadata.file_size_bytes == 1024
        assert metadata.source_filename == "test.pdf"

    def test_optional_fields_default_none(self):
        """Test optional fields default to None."""
        metadata = DocumentMetadata(
            file_format=FileFormat.PDF,
            file_size_bytes=1024,
            source_filename="test.pdf"
        )
        assert metadata.title is None
        assert metadata.author is None
        assert metadata.created_date is None
        assert metadata.modified_date is None
        assert metadata.page_count is None


class TestExtractionResult:
    """Tests for ExtractionResult model."""

    def test_create_with_minimal_fields(self):
        """Test ExtractionResult creation with minimal required fields."""
        metadata = DocumentMetadata(
            file_format=FileFormat.PDF,
            file_size_bytes=1024,
            source_filename="test.pdf"
        )
        result = ExtractionResult(markdown="", metadata=metadata)
        assert result.markdown == ""
        assert result.metadata == metadata

    def test_serializes_to_json(self):
        """Test ExtractionResult serializes to JSON correctly."""
        metadata = DocumentMetadata(
            file_format=FileFormat.PDF,
            file_size_bytes=1024,
            source_filename="test.pdf"
        )
        result = ExtractionResult(markdown="# Title", metadata=metadata)
        json_str = result.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["markdown"] == "# Title"
        assert parsed["metadata"]["file_format"] == "pdf"
        assert parsed["tables"] == []
        assert parsed["images"] == []
        assert parsed["errors"] == []

    def test_tables_default_empty_list(self):
        """Test tables field defaults to empty list."""
        metadata = DocumentMetadata(
            file_format=FileFormat.PDF,
            file_size_bytes=1024,
            source_filename="test.pdf"
        )
        result = ExtractionResult(markdown="", metadata=metadata)
        assert result.tables == []

    def test_images_default_empty_list(self):
        """Test images field defaults to empty list."""
        metadata = DocumentMetadata(
            file_format=FileFormat.PDF,
            file_size_bytes=1024,
            source_filename="test.pdf"
        )
        result = ExtractionResult(markdown="", metadata=metadata)
        assert result.images == []

    def test_errors_default_empty_list(self):
        """Test errors field defaults to empty list."""
        metadata = DocumentMetadata(
            file_format=FileFormat.PDF,
            file_size_bytes=1024,
            source_filename="test.pdf"
        )
        result = ExtractionResult(markdown="", metadata=metadata)
        assert result.errors == []

    def test_validation_catches_bad_types(self):
        """Test Pydantic validation catches type errors."""
        metadata = DocumentMetadata(
            file_format=FileFormat.PDF,
            file_size_bytes=1024,
            source_filename="test.pdf"
        )
        with pytest.raises(ValidationError):
            ExtractionResult(markdown=123, metadata=metadata)
