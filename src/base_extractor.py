"""
Abstract base class for document extractors.

Every supported file format implements this interface. The Strategy pattern
allows the DocumentRouter to dispatch to the correct extractor without
knowing format-specific details. Adding a new format means creating a
new class that inherits from BaseExtractor - no existing code changes.
"""

# TODO: Uncomment when implementing
# from abc import ABC, abstractmethod
# from pathlib import Path
# from .models import ExtractionResult, DocumentMetadata, TableData, ImageData, FileFormat


class BaseExtractor:
    """Abstract base class for all document format extractors.

    Subclasses must implement the four extraction methods.
    The extract_all() method orchestrates them into a unified result.

    Implementation notes:
    - Inherit from ABC
    - Mark extract_text, extract_tables, extract_images, extract_metadata as @abstractmethod
    - extract_all() should be fully implemented here (not abstract)
    """

    def __init__(self, file_path) -> None:
        """Initialize extractor with the path to the document.

        Args:
            file_path: Path to the document file. Must exist and be readable.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file path is not a file.

        Implementation notes:
        - Convert file_path to Path object
        - Store as self.file_path
        - Check exists() and is_file()
        - Raise appropriate exceptions with descriptive messages
        """
        # TODO: Implement file validation
        pass

    def extract_text(self) -> str:
        """Extract document text content as clean markdown.

        Returns:
            Document content formatted as markdown with heading
            hierarchy preserved.

        Implementation notes:
        - Mark as @abstractmethod
        - Subclasses implement format-specific extraction
        """
        # TODO: Mark as abstract
        pass

    def extract_tables(self) -> list:
        """Extract all tables from the document.

        Returns:
            List of TableData objects, each containing a 2D array
            of cell values.

        Implementation notes:
        - Mark as @abstractmethod
        - Return type should be list[TableData]
        """
        # TODO: Mark as abstract
        pass

    def extract_images(self) -> list:
        """Extract metadata for all images in the document.

        Returns:
            List of ImageData objects with available metadata.

        Implementation notes:
        - Mark as @abstractmethod
        - Return type should be list[ImageData]
        """
        # TODO: Mark as abstract
        pass

    def extract_metadata(self) -> object:
        """Extract document-level metadata.

        Returns:
            DocumentMetadata with available fields populated.

        Implementation notes:
        - Mark as @abstractmethod
        - Return type should be DocumentMetadata
        """
        # TODO: Mark as abstract
        pass

    def extract_all(self) -> object:
        """Run all extraction methods and return unified result.

        Implements partial success - individual extraction failures
        are captured in the errors list rather than raising exceptions.

        Returns:
            ExtractionResult containing all extractable content
            and a list of any non-fatal errors encountered.

        Implementation notes:
        - NOT abstract - implement fully in base class
        - Initialize empty errors list
        - Wrap each extract_* call in try/except
        - On exception, append to errors and use default (empty string, empty list)
        - For metadata failure, create minimal DocumentMetadata with UNKNOWN format
        - Return ExtractionResult with all collected data
        """
        # TODO: Implement orchestration with error handling
        pass
