"""
Tests for PPTX extractor stub.
"""

import pytest

# TODO: Uncomment when implementing
# from src.extractors import PPTXExtractor
# from src.models import ExtractionResult


class TestPPTXExtractorInit:
    """Tests for PPTXExtractor initialization."""

    def test_can_instantiate(self, tmp_pptx):
        """Test PPTXExtractor can be instantiated.

        Implementation:
        - Create PPTXExtractor(tmp_pptx)
        - Assert no exception raised
        """
        # TODO: Implement test
        pass


class TestPPTXExtractTextStub:
    """Tests for PPTX extract_text stub."""

    def test_raises_not_implemented(self, tmp_pptx):
        """Test extract_text raises NotImplementedError.

        Implementation:
        - Create extractor with tmp_pptx
        - Call extract_text()
        - Assert raises NotImplementedError
        """
        # TODO: Implement test
        pass

    def test_error_message_is_descriptive(self, tmp_pptx):
        """Test NotImplementedError has descriptive message.

        Implementation:
        - Create extractor with tmp_pptx
        - Try extract_text(), catch NotImplementedError
        - Assert "not yet implemented" in str(error).lower()
        """
        # TODO: Implement test
        pass


class TestPPTXExtractTablesStub:
    """Tests for PPTX extract_tables stub."""

    def test_raises_not_implemented(self, tmp_pptx):
        """Test extract_tables raises NotImplementedError.

        Implementation:
        - Create extractor with tmp_pptx
        - Call extract_tables()
        - Assert raises NotImplementedError
        """
        # TODO: Implement test
        pass


class TestPPTXExtractImagesStub:
    """Tests for PPTX extract_images stub."""

    def test_raises_not_implemented(self, tmp_pptx):
        """Test extract_images raises NotImplementedError.

        Implementation:
        - Create extractor with tmp_pptx
        - Call extract_images()
        - Assert raises NotImplementedError
        """
        # TODO: Implement test
        pass


class TestPPTXExtractMetadataStub:
    """Tests for PPTX extract_metadata stub."""

    def test_raises_not_implemented(self, tmp_pptx):
        """Test extract_metadata raises NotImplementedError.

        Implementation:
        - Create extractor with tmp_pptx
        - Call extract_metadata()
        - Assert raises NotImplementedError
        """
        # TODO: Implement test
        pass


class TestPPTXExtractAll:
    """Tests for PPTX extract_all override."""

    def test_returns_result_not_exception(self, tmp_pptx):
        """Test extract_all returns ExtractionResult, not exception.

        Implementation:
        - Create extractor with tmp_pptx
        - Call extract_all()
        - Assert returns ExtractionResult (no exception)
        """
        # TODO: Implement test
        pass

    def test_result_has_error_message(self, tmp_pptx):
        """Test result contains error about not implemented.

        Implementation:
        - Create extractor with tmp_pptx
        - Call extract_all()
        - Assert len(result.errors) > 0
        - Assert "pptx" in result.errors[0].lower()
        """
        # TODO: Implement test
        pass

    def test_result_has_empty_content(self, tmp_pptx):
        """Test result has empty markdown, tables, images.

        Implementation:
        - Create extractor with tmp_pptx
        - Call extract_all()
        - Assert result.markdown == ""
        - Assert result.tables == []
        - Assert result.images == []
        """
        # TODO: Implement test
        pass
