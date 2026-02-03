"""
Tests for XLSX extractor stub.
"""

import pytest

# TODO: Uncomment when implementing
# from src.extractors import XLSXExtractor
# from src.models import ExtractionResult


class TestXLSXExtractorInit:
    """Tests for XLSXExtractor initialization."""

    def test_can_instantiate(self, tmp_xlsx):
        """Test XLSXExtractor can be instantiated.

        Implementation:
        - Create XLSXExtractor(tmp_xlsx)
        - Assert no exception raised
        """
        # TODO: Implement test
        pass


class TestXLSXExtractTextStub:
    """Tests for XLSX extract_text stub."""

    def test_raises_not_implemented(self, tmp_xlsx):
        """Test extract_text raises NotImplementedError.

        Implementation:
        - Create extractor with tmp_xlsx
        - Call extract_text()
        - Assert raises NotImplementedError
        """
        # TODO: Implement test
        pass

    def test_error_message_is_descriptive(self, tmp_xlsx):
        """Test NotImplementedError has descriptive message.

        Implementation:
        - Create extractor with tmp_xlsx
        - Try extract_text(), catch NotImplementedError
        - Assert "not yet implemented" in str(error).lower()
        """
        # TODO: Implement test
        pass


class TestXLSXExtractTablesStub:
    """Tests for XLSX extract_tables stub."""

    def test_raises_not_implemented(self, tmp_xlsx):
        """Test extract_tables raises NotImplementedError.

        Implementation:
        - Create extractor with tmp_xlsx
        - Call extract_tables()
        - Assert raises NotImplementedError
        """
        # TODO: Implement test
        pass


class TestXLSXExtractImagesStub:
    """Tests for XLSX extract_images stub."""

    def test_raises_not_implemented(self, tmp_xlsx):
        """Test extract_images raises NotImplementedError.

        Implementation:
        - Create extractor with tmp_xlsx
        - Call extract_images()
        - Assert raises NotImplementedError
        """
        # TODO: Implement test
        pass


class TestXLSXExtractMetadataStub:
    """Tests for XLSX extract_metadata stub."""

    def test_raises_not_implemented(self, tmp_xlsx):
        """Test extract_metadata raises NotImplementedError.

        Implementation:
        - Create extractor with tmp_xlsx
        - Call extract_metadata()
        - Assert raises NotImplementedError
        """
        # TODO: Implement test
        pass


class TestXLSXExtractAll:
    """Tests for XLSX extract_all override."""

    def test_returns_result_not_exception(self, tmp_xlsx):
        """Test extract_all returns ExtractionResult, not exception.

        Implementation:
        - Create extractor with tmp_xlsx
        - Call extract_all()
        - Assert returns ExtractionResult (no exception)
        """
        # TODO: Implement test
        pass

    def test_result_has_error_message(self, tmp_xlsx):
        """Test result contains error about not implemented.

        Implementation:
        - Create extractor with tmp_xlsx
        - Call extract_all()
        - Assert len(result.errors) > 0
        - Assert "xlsx" in result.errors[0].lower()
        """
        # TODO: Implement test
        pass

    def test_result_has_empty_content(self, tmp_xlsx):
        """Test result has empty markdown, tables, images.

        Implementation:
        - Create extractor with tmp_xlsx
        - Call extract_all()
        - Assert result.markdown == ""
        - Assert result.tables == []
        - Assert result.images == []
        """
        # TODO: Implement test
        pass
