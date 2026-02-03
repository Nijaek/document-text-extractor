"""
Abstract base class for document extractors.

Every supported file format implements this interface. The Strategy pattern
allows the DocumentRouter to dispatch to the correct extractor without
knowing format-specific details. Adding a new format means creating a
new class that inherits from BaseExtractor — no existing code changes.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from .models import (
    ExtractionResult,
    DocumentMetadata,
    TableData,
    ImageData,
    FileFormat,
)


class BaseExtractor(ABC):
    """Abstract base class for all document format extractors.

    Subclasses must implement the four extraction methods.
    The `extract_all()` method orchestrates them into a unified result.
    """

    def __init__(self, file_path: Path | str) -> None:
        """Initialize extractor with the path to the document.

        Args:
            file_path: Path to the document file. Must exist and be readable.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file path is not a file.
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        if not self.file_path.is_file():
            raise ValueError(f"Path is not a file: {self.file_path}")

    @abstractmethod
    def extract_text(self) -> str:
        """Extract document text content as clean markdown.

        Returns:
            Document content formatted as markdown with heading
            hierarchy preserved.
        """
        ...

    @abstractmethod
    def extract_tables(self) -> list[TableData]:
        """Extract all tables from the document.

        Returns:
            List of TableData objects, each containing a 2D array
            of cell values.
        """
        ...

    @abstractmethod
    def extract_images(self) -> list[ImageData]:
        """Extract metadata for all images in the document.

        Returns:
            List of ImageData objects with available metadata.
        """
        ...

    @abstractmethod
    def extract_metadata(self) -> DocumentMetadata:
        """Extract document-level metadata.

        Returns:
            DocumentMetadata with available fields populated.
        """
        ...

    def extract_all(self) -> ExtractionResult:
        """Run all extraction methods and return unified result.

        Implements partial success — individual extraction failures
        are captured in the errors list rather than raising exceptions.

        Returns:
            ExtractionResult containing all extractable content
            and a list of any non-fatal errors encountered.
        """
        errors: list[str] = []

        # Extract text (critical — if this fails, report but continue)
        try:
            markdown = self.extract_text()
        except Exception as e:
            markdown = ""
            errors.append(f"Text extraction failed: {e}")

        # Extract tables
        try:
            tables = self.extract_tables()
        except Exception as e:
            tables = []
            errors.append(f"Table extraction failed: {e}")

        # Extract images
        try:
            images = self.extract_images()
        except Exception as e:
            images = []
            errors.append(f"Image extraction failed: {e}")

        # Extract metadata (should rarely fail, but protect anyway)
        try:
            metadata = self.extract_metadata()
        except Exception as e:
            # Metadata is required by the model, so build a minimal one
            metadata = DocumentMetadata(
                file_format=FileFormat.UNKNOWN,
                file_size_bytes=self.file_path.stat().st_size,
                source_filename=self.file_path.name,
            )
            errors.append(f"Metadata extraction failed: {e}")

        return ExtractionResult(
            markdown=markdown,
            tables=tables,
            images=images,
            metadata=metadata,
            errors=errors,
        )
