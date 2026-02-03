"""
PPTX document extractor using python-pptx.

NOTE: This extractor is a documented stub, not a full implementation.
This is a deliberate scoping decision. The architecture fully supports
PPTX extraction - implementation follows the same BaseExtractor pattern.
"""

# TODO: Uncomment when implementing
# from pptx import Presentation
# from pathlib import Path
# from ..base_extractor import BaseExtractor
# from ..models import TableData, ImageData, DocumentMetadata, FileFormat, ExtractionResult
# from ..logging_config import get_logger

# logger = get_logger(__name__)


class PPTXExtractor:
    """Extracts content from PPTX presentations.

    NOTE: This is a stub implementation. All extraction methods raise
    NotImplementedError with descriptive messages about the implementation
    approach.

    Implementation notes:
    - Inherit from BaseExtractor
    - Override extract_all() to return result with error instead of raising
    """

    def __init__(self, file_path) -> None:
        """Initialize PPTX extractor.

        Args:
            file_path: Path to PPTX file.

        Implementation notes:
        - Call super().__init__(file_path)
        - Could load presentation here: Presentation(file_path)
        """
        # TODO: Initialize with parent class
        pass

    def extract_text(self) -> str:
        """Extract text from all slides as markdown.

        Implementation approach (not yet implemented):
        - Load presentation with Presentation(file_path)
        - Iterate through presentation.slides
        - For each slide, iterate through slide.shapes
        - For text frames (shape.has_text_frame), extract paragraphs
        - Map slide titles to H2 headings
        - Preserve bullet/numbered list formatting
        - Separate slides with horizontal rules (---)

        Raises:
            NotImplementedError: Always, as this is a stub.
        """
        # TODO: Raise NotImplementedError with descriptive message
        pass

    def extract_tables(self) -> list:
        """Extract all tables from the presentation.

        Implementation approach (not yet implemented):
        - Iterate through slides
        - For each slide, check shapes for tables (shape.has_table)
        - Extract cell values into 2D array
        - Record slide number

        Raises:
            NotImplementedError: Always, as this is a stub.
        """
        # TODO: Raise NotImplementedError with descriptive message
        pass

    def extract_images(self) -> list:
        """Extract metadata for all images.

        Implementation approach (not yet implemented):
        - Iterate through slides
        - For each slide, check shapes for images
        - Access image through shape.image
        - Get dimensions, format, generate filename
        - Record slide number

        Raises:
            NotImplementedError: Always, as this is a stub.
        """
        # TODO: Raise NotImplementedError with descriptive message
        pass

    def extract_metadata(self) -> object:
        """Extract presentation metadata.

        Implementation approach (not yet implemented):
        - Access presentation.core_properties
        - Map: title, author, created, modified
        - Slide count: len(presentation.slides)
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
        - Create minimal DocumentMetadata with FileFormat.PPTX
        - Return ExtractionResult with:
          - markdown = ""
          - tables = []
          - images = []
          - errors = ["PPTX extraction not yet implemented..."]
        """
        # TODO: Return stub result instead of raising
        pass
