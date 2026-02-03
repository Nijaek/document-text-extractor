"""
Tests for DocumentRouter.
"""

import pytest

# TODO: Uncomment when implementing
# from src.router import DocumentRouter, process_document
# from src.extractors import PDFExtractor, DOCXExtractor, PPTXExtractor


class TestDocumentRouter:
    """Tests for DocumentRouter class."""

    def test_returns_pdf_extractor_for_pdf(self, tmp_pdf):
        """Test router returns PDFExtractor for .pdf files.

        Implementation:
        - Create router
        - Call get_extractor(tmp_pdf)
        - Assert isinstance(result, PDFExtractor)
        """
        # TODO: Implement test
        pass

    def test_returns_docx_extractor_for_docx(self, tmp_docx):
        """Test router returns DOCXExtractor for .docx files.

        Implementation:
        - Create router
        - Call get_extractor(tmp_docx)
        - Assert isinstance(result, DOCXExtractor)
        """
        # TODO: Implement test
        pass

    def test_returns_pptx_extractor_for_pptx(self, tmp_pptx):
        """Test router returns PPTXExtractor for .pptx files.

        Implementation:
        - Create router
        - Call get_extractor(tmp_pptx)
        - Assert isinstance(result, PPTXExtractor)
        """
        # TODO: Implement test
        pass

    def test_raises_value_error_for_unsupported_extension(self, tmp_path):
        """Test router raises ValueError for unsupported formats.

        Implementation:
        - Create file with .xyz extension
        - Call get_extractor()
        - Assert raises ValueError
        """
        # TODO: Implement test
        pass

    def test_raises_file_not_found_for_missing_file(self):
        """Test router raises FileNotFoundError for non-existent files.

        Implementation:
        - Call get_extractor with non-existent path
        - Assert raises FileNotFoundError
        """
        # TODO: Implement test
        pass

    def test_supported_formats_returns_list(self):
        """Test supported_formats returns list of formats.

        Implementation:
        - Call DocumentRouter.supported_formats()
        - Assert result is list
        - Assert contains expected formats
        """
        # TODO: Implement test
        pass

    def test_unsupported_format_error_contains_extension(self, tmp_path):
        """Test error message contains the invalid extension.

        Implementation:
        - Create file with .xyz extension
        - Call get_extractor()
        - Catch ValueError
        - Assert ".xyz" in error message
        """
        # TODO: Implement test
        pass

    def test_unsupported_format_error_lists_supported(self, tmp_path):
        """Test error message lists supported formats.

        Implementation:
        - Create file with .xyz extension
        - Call get_extractor()
        - Catch ValueError
        - Assert ".pdf" in error message
        - Assert ".docx" in error message
        """
        # TODO: Implement test
        pass


class TestProcessDocument:
    """Tests for process_document convenience function."""

    def test_returns_extraction_result(self, tmp_pdf):
        """Test process_document returns ExtractionResult.

        Implementation:
        - Call process_document(tmp_pdf)
        - Assert result is ExtractionResult instance
        """
        # TODO: Implement test
        pass

    def test_works_with_string_path(self, tmp_pdf):
        """Test process_document accepts string path.

        Implementation:
        - Call process_document(str(tmp_pdf))
        - Assert no error and returns result
        """
        # TODO: Implement test
        pass
