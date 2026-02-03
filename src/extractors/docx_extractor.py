"""
DOCX document extractor using python-docx.

Handles Microsoft Word documents (.docx format).
"""

from pathlib import Path

from ..base_extractor import BaseExtractor
from ..models import TableData, ImageData, DocumentMetadata, FileFormat, ExtractionResult


class DOCXExtractor(BaseExtractor):
    """Extracts content from DOCX documents.

    Uses python-docx for all extraction operations.

    NOTE: This is a stub implementation. The extract_all() method returns
    a result with an error message indicating the extractor is not yet implemented.
    """

    def __init__(self, file_path: Path | str) -> None:
        """Initialize DOCX extractor.

        Args:
            file_path: Path to DOCX file.
        """
        super().__init__(file_path)

    def extract_text(self) -> str:
        """Extract document text as markdown.

        Returns:
            Clean markdown string with heading hierarchy preserved.

        Raises:
            NotImplementedError: DOCX extraction not yet implemented.
        """
        raise NotImplementedError("DOCX text extraction not yet implemented")

    def extract_tables(self) -> list[TableData]:
        """Extract all tables from the document.

        Returns:
            List of TableData objects.

        Raises:
            NotImplementedError: DOCX extraction not yet implemented.
        """
        raise NotImplementedError("DOCX table extraction not yet implemented")

    def extract_images(self) -> list[ImageData]:
        """Extract metadata for all images.

        Returns:
            List of ImageData objects.

        Raises:
            NotImplementedError: DOCX extraction not yet implemented.
        """
        raise NotImplementedError("DOCX image extraction not yet implemented")

    def extract_metadata(self) -> DocumentMetadata:
        """Extract document metadata.

        Returns:
            DocumentMetadata object.

        Raises:
            NotImplementedError: DOCX extraction not yet implemented.
        """
        raise NotImplementedError("DOCX metadata extraction not yet implemented")

    def extract_all(self) -> ExtractionResult:
        """Return result with error indicating not yet implemented.

        Overrides BaseExtractor to return a stub result instead of
        calling individual extraction methods.

        Returns:
            ExtractionResult with empty content and error message.
        """
        return ExtractionResult(
            markdown="",
            tables=[],
            images=[],
            metadata=DocumentMetadata(
                file_format=FileFormat.DOCX,
                file_size_bytes=self.file_path.stat().st_size,
                source_filename=self.file_path.name,
            ),
            errors=["DOCX extraction not yet implemented. File was recognized but content extraction is pending."],
        )
