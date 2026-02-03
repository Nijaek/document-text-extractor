"""
XLSX document extractor using openpyxl.

NOTE: This extractor is a documented stub, not a full implementation.
This is a deliberate scoping decision. The architecture fully supports
XLSX extraction - implementation follows the same BaseExtractor pattern.

Excel files are workbook-based with multiple sheets, each containing cells.
This is different from page/paragraph/slide-based formats.
"""

# TODO: Uncomment when implementing
# from openpyxl import load_workbook
# from pathlib import Path
# from ..base_extractor import BaseExtractor
# from ..models import TableData, ImageData, DocumentMetadata, FileFormat, ExtractionResult
# from ..logging_config import get_logger

# logger = get_logger(__name__)


class XLSXExtractor:
    """Extracts content from XLSX workbooks.

    NOTE: This is a stub implementation. All extraction methods raise
    NotImplementedError with descriptive messages about the implementation
    approach.

    Implementation notes:
    - Inherit from BaseExtractor
    - Override extract_all() to return result with error instead of raising
    """

    def __init__(self, file_path) -> None:
        """Initialize XLSX extractor.

        Args:
            file_path: Path to XLSX file.

        Implementation notes:
        - Call super().__init__(file_path)
        - Could load workbook here: load_workbook(file_path)
        """
        # TODO: Initialize with parent class
        pass

    def extract_text(self) -> str:
        """Extract text from all sheets as markdown.

        Implementation approach (not yet implemented):
        - Load workbook with openpyxl.load_workbook(file_path)
        - Iterate through workbook.sheetnames
        - For each sheet, iterate through rows (sheet.iter_rows())
        - Convert cell values to strings
        - Use sheet names as H2 headings
        - Separate sheets with horizontal rules (---)

        Raises:
            NotImplementedError: Always, as this is a stub.
        """
        # TODO: Raise NotImplementedError with descriptive message
        pass

    def extract_tables(self) -> list:
        """Extract all tables from the workbook.

        Implementation approach (not yet implemented):
        - Each sheet is essentially a table
        - Could treat each sheet as a TableData with sheet name as caption
        - Or detect distinct table regions within sheets using data bounds
        - Use sheet.max_row and sheet.max_column to determine dimensions

        Raises:
            NotImplementedError: Always, as this is a stub.
        """
        # TODO: Raise NotImplementedError with descriptive message
        pass

    def extract_images(self) -> list:
        """Extract metadata for all images.

        Implementation approach (not yet implemented):
        - Iterate through sheets
        - Access images via worksheet._images
        - Extract dimensions and format from image objects
        - Generate filename with sheet name and index

        Raises:
            NotImplementedError: Always, as this is a stub.
        """
        # TODO: Raise NotImplementedError with descriptive message
        pass

    def extract_metadata(self) -> object:
        """Extract workbook metadata.

        Implementation approach (not yet implemented):
        - Use workbook.properties for title, author, created, modified
        - Sheet count from len(workbook.sheetnames)
        - File size from path

        Raises:
            NotImplementedError: Always, as this is a stub.
        """
        # TODO: Raise NotImplementedError with descriptive message
        pass

    def extract_all(self) -> object:
        """Override to return result with error instead of raising.

        Returns:
            ExtractionResult with empty content and error message.

        Implementation notes:
        - Do NOT call parent's extract_all() (it would catch NotImplementedError)
        - Create minimal DocumentMetadata with FileFormat.XLSX
        - Return ExtractionResult with:
          - markdown = ""
          - tables = []
          - images = []
          - errors = ["XLSX extraction not yet implemented..."]
        """
        # TODO: Return stub result instead of raising
        pass
