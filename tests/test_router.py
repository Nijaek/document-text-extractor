"""
Tests for DocumentRouter.
"""

import pytest

from src.router import DocumentRouter, process_document
from src.extractors import PDFExtractor, DOCXExtractor, PPTXExtractor, XLSXExtractor
from src.models import ExtractionResult


class TestDocumentRouter:
    """Tests for DocumentRouter class."""

    def test_returns_pdf_extractor_for_pdf(self, tmp_pdf):
        """Test router returns PDFExtractor for .pdf files."""
        router = DocumentRouter()
        extractor = router.get_extractor(tmp_pdf)
        assert isinstance(extractor, PDFExtractor)

    def test_returns_docx_extractor_for_docx(self, tmp_docx):
        """Test router returns DOCXExtractor for .docx files."""
        router = DocumentRouter()
        extractor = router.get_extractor(tmp_docx)
        assert isinstance(extractor, DOCXExtractor)

    def test_returns_pptx_extractor_for_pptx(self, tmp_pptx):
        """Test router returns PPTXExtractor for .pptx files."""
        router = DocumentRouter()
        extractor = router.get_extractor(tmp_pptx)
        assert isinstance(extractor, PPTXExtractor)

    def test_returns_xlsx_extractor_for_xlsx(self, tmp_xlsx):
        """Test router returns XLSXExtractor for .xlsx files."""
        router = DocumentRouter()
        extractor = router.get_extractor(tmp_xlsx)
        assert isinstance(extractor, XLSXExtractor)

    def test_raises_value_error_for_unsupported_extension(self, tmp_path):
        """Test router raises ValueError for unsupported formats."""
        unsupported_file = tmp_path / "test.xyz"
        unsupported_file.write_text("dummy content")

        router = DocumentRouter()
        with pytest.raises(ValueError):
            router.get_extractor(unsupported_file)

    def test_raises_file_not_found_for_missing_file(self):
        """Test router raises FileNotFoundError for non-existent files."""
        router = DocumentRouter()
        with pytest.raises(FileNotFoundError):
            router.get_extractor("/nonexistent/path/file.pdf")

    def test_supported_formats_returns_list(self):
        """Test supported_formats returns list of formats."""
        formats = DocumentRouter.supported_formats()
        assert isinstance(formats, list)
        assert ".pdf" in formats
        assert ".docx" in formats
        assert ".pptx" in formats
        assert ".xlsx" in formats

    def test_unsupported_format_error_contains_extension(self, tmp_path):
        """Test error message contains the invalid extension."""
        unsupported_file = tmp_path / "test.xyz"
        unsupported_file.write_text("dummy content")

        router = DocumentRouter()
        with pytest.raises(ValueError) as exc_info:
            router.get_extractor(unsupported_file)
        assert ".xyz" in str(exc_info.value)

    def test_unsupported_format_error_lists_supported(self, tmp_path):
        """Test error message lists supported formats."""
        unsupported_file = tmp_path / "test.xyz"
        unsupported_file.write_text("dummy content")

        router = DocumentRouter()
        with pytest.raises(ValueError) as exc_info:
            router.get_extractor(unsupported_file)
        error_message = str(exc_info.value)
        assert ".pdf" in error_message
        assert ".docx" in error_message

    def test_case_insensitive_extension(self, tmp_path):
        """Test router handles uppercase extensions."""
        # Create a PDF with uppercase extension
        import fitz
        doc = fitz.open()
        doc.new_page()
        pdf_path = tmp_path / "test.PDF"
        doc.save(pdf_path)
        doc.close()

        router = DocumentRouter()
        extractor = router.get_extractor(pdf_path)
        assert isinstance(extractor, PDFExtractor)

    def test_process_document_returns_extraction_result(self, tmp_pdf):
        """Test process_document method returns ExtractionResult."""
        router = DocumentRouter()
        result = router.process_document(tmp_pdf)
        assert isinstance(result, ExtractionResult)

    def test_process_document_with_stub_extractor(self, tmp_docx):
        """Test process_document works with stub extractors."""
        router = DocumentRouter()
        result = router.process_document(tmp_docx)
        assert isinstance(result, ExtractionResult)
        # Stub should return an error message
        assert len(result.errors) > 0
        assert "not yet implemented" in result.errors[0].lower()


class TestProcessDocument:
    """Tests for process_document convenience function."""

    def test_returns_extraction_result(self, tmp_pdf):
        """Test process_document returns ExtractionResult."""
        result = process_document(tmp_pdf)
        assert isinstance(result, ExtractionResult)

    def test_works_with_string_path(self, tmp_pdf):
        """Test process_document accepts string path."""
        result = process_document(str(tmp_pdf))
        assert isinstance(result, ExtractionResult)

    def test_extracts_content_from_pdf(self, tmp_pdf):
        """Test process_document extracts actual content."""
        result = process_document(tmp_pdf)
        # The tmp_pdf fixture contains "Test Document Title"
        assert "Test Document Title" in result.markdown

    def test_raises_for_unsupported_format(self, tmp_path):
        """Test process_document raises ValueError for unsupported formats."""
        unsupported_file = tmp_path / "test.xyz"
        unsupported_file.write_text("dummy")
        with pytest.raises(ValueError):
            process_document(unsupported_file)

    def test_raises_for_missing_file(self):
        """Test process_document raises FileNotFoundError for missing files."""
        with pytest.raises(FileNotFoundError):
            process_document("/nonexistent/file.pdf")
