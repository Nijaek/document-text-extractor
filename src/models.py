"""
Data models for the document extraction system.

All extractors produce ExtractionResult as their output, ensuring
a uniform interface regardless of input document format.
"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class FileFormat(str, Enum):
    """Supported document formats."""
    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    XLSX = "xlsx"
    UNKNOWN = "unknown"


class TableData(BaseModel):
    """Represents a single extracted table.

    Content is stored as a 2D array (list of rows, each row is a list of cell strings).
    This preserves row-column relationships for downstream processing,
    which is critical for LLM reasoning over tabular data.
    """
    content: list[list[str]] = Field(
        description="2D array of cell values. First row is typically headers."
    )
    page_or_slide: int | None = Field(
        default=None,
        description="Page number (PDF) or slide number (PPTX) where table appears."
    )
    caption: str | None = Field(
        default=None,
        description="Table caption if available in the source document."
    )


class ImageData(BaseModel):
    """Represents a single extracted image and its metadata.

    In v1, only metadata is extracted (no AI-generated descriptions).
    The description field is reserved for future integration with
    a vision model for automatic captioning.
    """
    filename: str = Field(
        description="Generated filename for the extracted image."
    )
    format: str = Field(
        description="Image format (png, jpg, etc.)."
    )
    width: int | None = Field(
        default=None,
        description="Image width in pixels."
    )
    height: int | None = Field(
        default=None,
        description="Image height in pixels."
    )
    alt_text: str | None = Field(
        default=None,
        description="Alt text from the source document, if available."
    )
    description: str | None = Field(
        default=None,
        description="AI-generated description. Reserved for v2."
    )
    page_or_slide: int | None = Field(
        default=None,
        description="Page or slide number where image appears."
    )


class DocumentMetadata(BaseModel):
    """Metadata about the source document itself."""
    title: str | None = None
    author: str | None = None
    created_date: datetime | None = None
    modified_date: datetime | None = None
    page_count: int | None = None
    file_format: FileFormat
    file_size_bytes: int
    source_filename: str


class ExtractionResult(BaseModel):
    """Unified output from any document extractor.

    Designed for partial success — the errors field captures non-fatal
    issues so that usable content is always returned even if some
    elements fail to extract. This is critical in enterprise pipelines
    where a single corrupt table shouldn't prevent processing 49 clean pages.
    """
    markdown: str = Field(
        description="Full document content as clean markdown."
    )
    tables: list[TableData] = Field(
        default_factory=list,
        description="All tables extracted from the document."
    )
    images: list[ImageData] = Field(
        default_factory=list,
        description="Metadata for all images found in the document."
    )
    metadata: DocumentMetadata
    errors: list[str] = Field(
        default_factory=list,
        description="Non-fatal errors encountered during extraction."
    )
