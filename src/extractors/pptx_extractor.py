"""
PPTX document extractor using python-pptx.

NOTE: This extractor is a documented stub, not a full implementation.
This is a deliberate scoping decision. The architecture fully supports
PPTX extraction - implementation follows the same BaseExtractor pattern.
"""

from pathlib import Path

from ..base_extractor import BaseExtractor
from ..models import TableData, ImageData, DocumentMetadata, FileFormat, ExtractionResult


class PPTXExtractor(BaseExtractor):
    """Extracts content from PPTX presentations.

    NOTE: This is a stub implementation. The extract_all() method returns
    a result with an error message indicating the extractor is not yet implemented.
    """

    def __init__(self, file_path: Path | str) -> None:
        """Initialize PPTX extractor.

        Args:
            file_path: Path to PPTX file.
        """
        super().__init__(file_path)

    def extract_text(self) -> str:
        """Extract text from all slides as markdown.

        Raises:
            NotImplementedError: PPTX extraction not yet implemented.
        """
        raise NotImplementedError("PPTX text extraction not yet implemented")

    def extract_tables(self) -> list[TableData]:
        """Extract all tables from the presentation.

        Raises:
            NotImplementedError: PPTX extraction not yet implemented.
        """
        raise NotImplementedError("PPTX table extraction not yet implemented")

    def extract_images(self) -> list[ImageData]:
        """Extract metadata for all images.

        Raises:
            NotImplementedError: PPTX extraction not yet implemented.
        """
        raise NotImplementedError("PPTX image extraction not yet implemented")

    def extract_metadata(self) -> DocumentMetadata:
        """Extract presentation metadata.

        Raises:
            NotImplementedError: PPTX extraction not yet implemented.
        """
        raise NotImplementedError("PPTX metadata extraction not yet implemented")

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
                file_format=FileFormat.PPTX,
                file_size_bytes=self.file_path.stat().st_size,
                source_filename=self.file_path.name,
            ),
            errors=["PPTX extraction not yet implemented. File was recognized but content extraction is pending."],
        )
