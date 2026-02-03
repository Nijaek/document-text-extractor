"""
Data models for the document extraction system.

All extractors produce ExtractionResult as their output, ensuring
a uniform interface regardless of input document format.

Implementation notes:
- Use Pydantic's BaseModel for all models
- Use Field() with descriptions for documentation
- FileFormat should inherit from (str, Enum)
"""

# TODO: Uncomment when implementing
# from datetime import datetime
# from enum import Enum
# from pydantic import BaseModel, Field


class FileFormat:
    """Supported document formats.

    Implementation notes:
    - Inherit from (str, Enum)
    - Values:
        PDF = "pdf"
        DOCX = "docx"
        PPTX = "pptx"
        XLSX = "xlsx"
        UNKNOWN = "unknown"
    """
    # TODO: Implement as Enum
    pass


class TableData:
    """Represents a single extracted table.

    Content is stored as a 2D array (list of rows, each row is a list of cell strings).
    This preserves row-column relationships for downstream processing,
    which is critical for LLM reasoning over tabular data.

    Fields:
    - content: list[list[str]] - 2D array of cell values. First row is typically headers.
    - page_or_slide: int | None - Page number (PDF) or slide number (PPTX) where table appears.
    - caption: str | None - Table caption if available in the source document.

    Implementation notes:
    - Inherit from BaseModel
    - Use Field() with descriptions for each field
    """
    # TODO: Implement as Pydantic model
    pass


class ImageData:
    """Represents a single extracted image and its metadata.

    In v1, only metadata is extracted (no AI-generated descriptions).
    The description field is reserved for future integration with
    a vision model for automatic captioning.

    Fields:
    - filename: str - Generated filename for the extracted image.
    - format: str - Image format (png, jpg, etc.).
    - width: int | None - Image width in pixels.
    - height: int | None - Image height in pixels.
    - alt_text: str | None - Alt text from the source document, if available.
    - description: str | None - AI-generated description. Reserved for v2.
    - page_or_slide: int | None - Page or slide number where image appears.

    Implementation notes:
    - Inherit from BaseModel
    - Use Field() with descriptions and defaults
    """
    # TODO: Implement as Pydantic model
    pass


class DocumentMetadata:
    """Metadata about the source document itself.

    Fields:
    - title: str | None
    - author: str | None
    - created_date: datetime | None
    - modified_date: datetime | None
    - page_count: int | None
    - file_format: FileFormat
    - file_size_bytes: int
    - source_filename: str

    Implementation notes:
    - Inherit from BaseModel
    - file_format, file_size_bytes, source_filename are required
    - All other fields are optional (default None)
    """
    # TODO: Implement as Pydantic model
    pass


class ExtractionResult:
    """Unified output from any document extractor.

    Designed for partial success - the errors field captures non-fatal
    issues so that usable content is always returned even if some
    elements fail to extract. This is critical in enterprise pipelines
    where a single corrupt table shouldn't prevent processing 49 clean pages.

    Fields:
    - markdown: str - Full document content as clean markdown.
    - tables: list[TableData] - All tables extracted from the document.
    - images: list[ImageData] - Metadata for all images found in the document.
    - metadata: DocumentMetadata - Document-level metadata.
    - errors: list[str] - Non-fatal errors encountered during extraction.

    Implementation notes:
    - Inherit from BaseModel
    - Use Field() with descriptions
    - tables, images, errors should use default_factory=list
    - metadata is required
    """
    # TODO: Implement as Pydantic model
    pass
