"""
Tests for Pydantic data models.
"""

import pytest

# TODO: Uncomment when implementing
# from src.models import (
#     FileFormat,
#     TableData,
#     ImageData,
#     DocumentMetadata,
#     ExtractionResult,
# )


class TestFileFormat:
    """Tests for FileFormat enum."""

    def test_pdf_value(self):
        """Test FileFormat.PDF has correct value.

        Implementation:
        - Assert FileFormat.PDF.value == "pdf"
        """
        # TODO: Implement test
        pass

    def test_docx_value(self):
        """Test FileFormat.DOCX has correct value.

        Implementation:
        - Assert FileFormat.DOCX.value == "docx"
        """
        # TODO: Implement test
        pass

    def test_pptx_value(self):
        """Test FileFormat.PPTX has correct value.

        Implementation:
        - Assert FileFormat.PPTX.value == "pptx"
        """
        # TODO: Implement test
        pass

    def test_unknown_value(self):
        """Test FileFormat.UNKNOWN has correct value.

        Implementation:
        - Assert FileFormat.UNKNOWN.value == "unknown"
        """
        # TODO: Implement test
        pass


class TestTableData:
    """Tests for TableData model."""

    def test_create_with_content(self):
        """Test TableData creation with 2D content array.

        Implementation:
        - Create TableData with content=[["a", "b"], ["c", "d"]]
        - Assert content matches
        """
        # TODO: Implement test
        pass

    def test_optional_fields_default_none(self):
        """Test optional fields default to None.

        Implementation:
        - Create TableData with only content
        - Assert page_or_slide is None
        - Assert caption is None
        """
        # TODO: Implement test
        pass


class TestImageData:
    """Tests for ImageData model."""

    def test_create_with_required_fields(self):
        """Test ImageData creation with required fields.

        Implementation:
        - Create ImageData with filename="test.png", format="png"
        - Assert fields match
        """
        # TODO: Implement test
        pass

    def test_optional_fields_default_none(self):
        """Test optional fields default to None.

        Implementation:
        - Create ImageData with only required fields
        - Assert width, height, alt_text, description, page_or_slide are None
        """
        # TODO: Implement test
        pass


class TestDocumentMetadata:
    """Tests for DocumentMetadata model."""

    def test_create_with_required_fields(self):
        """Test DocumentMetadata creation with required fields.

        Implementation:
        - Create with file_format, file_size_bytes, source_filename
        - Assert fields match
        """
        # TODO: Implement test
        pass

    def test_optional_fields_default_none(self):
        """Test optional fields default to None.

        Implementation:
        - Create with only required fields
        - Assert title, author, created_date, modified_date, page_count are None
        """
        # TODO: Implement test
        pass


class TestExtractionResult:
    """Tests for ExtractionResult model."""

    def test_create_with_minimal_fields(self):
        """Test ExtractionResult creation with minimal required fields.

        Implementation:
        - Create with markdown="" and minimal metadata
        - Assert creation succeeds
        """
        # TODO: Implement test
        pass

    def test_serializes_to_json(self):
        """Test ExtractionResult serializes to JSON correctly.

        Implementation:
        - Create valid ExtractionResult
        - Call .model_dump_json()
        - Assert result is valid JSON string
        - Parse and verify structure
        """
        # TODO: Implement test
        pass

    def test_tables_default_empty_list(self):
        """Test tables field defaults to empty list.

        Implementation:
        - Create ExtractionResult without specifying tables
        - Assert tables == []
        """
        # TODO: Implement test
        pass

    def test_images_default_empty_list(self):
        """Test images field defaults to empty list.

        Implementation:
        - Create ExtractionResult without specifying images
        - Assert images == []
        """
        # TODO: Implement test
        pass

    def test_errors_default_empty_list(self):
        """Test errors field defaults to empty list.

        Implementation:
        - Create ExtractionResult without specifying errors
        - Assert errors == []
        """
        # TODO: Implement test
        pass

    def test_validation_catches_bad_types(self):
        """Test Pydantic validation catches type errors.

        Implementation:
        - Try to create with markdown=123 (int instead of str)
        - Assert ValidationError is raised
        """
        # TODO: Implement test
        pass
