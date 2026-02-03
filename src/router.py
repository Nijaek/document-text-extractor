"""
Document router for dispatching files to appropriate extractors.

The router's job is simple: take a file path, determine the format,
and return the correct extractor instance. Uses the Strategy pattern
to decouple format detection from extraction logic.
"""

# TODO: Uncomment when implementing
# from pathlib import Path
# from .models import FileFormat, ExtractionResult
# from .base_extractor import BaseExtractor
# from .extractors import PDFExtractor, DOCXExtractor, PPTXExtractor


class DocumentRouter:
    """Routes document files to their appropriate extractors.

    Uses a registry dict mapping FileFormat to extractor classes.
    This makes adding new formats trivial - just add to the registry.

    Implementation notes:
    - Create _EXTRACTOR_REGISTRY class attribute mapping FileFormat -> ExtractorClass
    - Example: {FileFormat.PDF: PDFExtractor, FileFormat.DOCX: DOCXExtractor, ...}
    """

    def __init__(self) -> None:
        """Initialize the document router.

        Implementation notes:
        - Could initialize registry here or use class attribute
        - No special setup needed for v1
        """
        # TODO: Initialize router
        pass

    def get_extractor(self, file_path) -> object:
        """Get the appropriate extractor for a file.

        Args:
            file_path: Path or str to the document file.

        Returns:
            Instantiated extractor ready to use (e.g., PDFExtractor).

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is not supported.

        Implementation notes:
        - Convert to Path object
        - Get extension with .suffix.lower().lstrip(".")
        - Try to match to FileFormat enum
        - On ValueError (unknown format), raise with helpful message:
          "Unsupported file format: '.xyz'. Supported formats: .pdf, .docx, .pptx"
        - Look up extractor class in registry
        - Return instantiated extractor with file_path
        """
        # TODO: Implement format detection and extractor instantiation
        pass

    @classmethod
    def supported_formats(cls) -> list:
        """Return list of supported file formats.

        Returns:
            List of FileFormat values that have registered extractors.

        Implementation notes:
        - Return keys from _EXTRACTOR_REGISTRY
        - Or return list of FileFormat enum values (excluding UNKNOWN)
        """
        # TODO: Implement
        pass


def process_document(file_path) -> object:
    """Convenience function for one-line document extraction.

    Args:
        file_path: Path or str to the document file.

    Returns:
        ExtractionResult from the appropriate extractor.

    Example:
        result = process_document("path/to/document.pdf")
        print(result.markdown)

    Implementation notes:
    - Create DocumentRouter instance
    - Call get_extractor(file_path)
    - Call extract_all() on the extractor
    - Return the result
    """
    # TODO: Implement convenience function
    pass
