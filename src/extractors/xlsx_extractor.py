"""
XLSX document extractor using openpyxl.

NOTE: This extractor is a documented stub, not a full implementation.
This is a deliberate scoping decision. The architecture fully supports
XLSX extraction - implementation follows the same BaseExtractor pattern.

Excel files are workbook-based with multiple sheets, each containing cells.
This is different from page/paragraph/slide-based formats.
"""

from pathlib import Path

from ..base_extractor import BaseExtractor
from ..models import TableData, ImageData, DocumentMetadata, FileFormat, ExtractionResult


class XLSXExtractor(BaseExtractor):
    """Extracts content from XLSX workbooks.

    NOTE: This is a stub implementation. The extract_all() method returns
    a result with an error message indicating the extractor is not yet implemented.
    """

    def __init__(self, file_path: Path | str) -> None:
        """Initialize XLSX extractor.

        Args:
            file_path: Path to XLSX file.
        """
        super().__init__(file_path)

    def extract_text(self) -> str:
        """Extract text from all sheets as markdown.

        Raises:
            NotImplementedError: XLSX extraction not yet implemented.
        """
        raise NotImplementedError("XLSX text extraction not yet implemented")

    def extract_tables(self) -> list[TableData]:
        """Extract all tables from the workbook.

        Raises:
            NotImplementedError: XLSX extraction not yet implemented.
        """
        raise NotImplementedError("XLSX table extraction not yet implemented")

    def extract_images(self) -> list[ImageData]:
        """Extract metadata for all images.

        Raises:
            NotImplementedError: XLSX extraction not yet implemented.
        """
        raise NotImplementedError("XLSX image extraction not yet implemented")

    def extract_metadata(self) -> DocumentMetadata:
        """Extract workbook metadata.

        Raises:
            NotImplementedError: XLSX extraction not yet implemented.
        """
        raise NotImplementedError("XLSX metadata extraction not yet implemented")

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
                file_format=FileFormat.XLSX,
                file_size_bytes=self.file_path.stat().st_size,
                source_filename=self.file_path.name,
            ),
            errors=["XLSX extraction not yet implemented. File was recognized but content extraction is pending."],
        )
