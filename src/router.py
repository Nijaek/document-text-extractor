"""
Document router for dispatching files to appropriate extractors.

The router's job is simple: take a file path, determine the format,
and return the correct extractor instance. Uses the Strategy pattern
to decouple format detection from extraction logic.
"""

from pathlib import Path

from .models import ExtractionResult, FileFormat
from .extractors.pdf_extractor import PDFExtractor
from .extractors.docx_extractor import DOCXExtractor
from .extractors.pptx_extractor import PPTXExtractor
from .extractors.xlsx_extractor import XLSXExtractor

# Map file extensions to (FileFormat, ExtractorClass)
EXTRACTOR_MAP = {
    ".pdf": (FileFormat.PDF, PDFExtractor),
    ".docx": (FileFormat.DOCX, DOCXExtractor),
    ".pptx": (FileFormat.PPTX, PPTXExtractor),
    ".xlsx": (FileFormat.XLSX, XLSXExtractor),
}


class DocumentRouter:
    """Routes document files to their appropriate extractors.

    Uses a registry dict mapping file extensions to extractor classes.
    This makes adding new formats trivial - just add to EXTRACTOR_MAP.

    Note: This class currently holds no state — instance methods could be
    static or module-level functions. The class structure is retained for
    future extensibility (e.g., adding configuration options like OCR settings
    or custom extractor registries) and to make the Strategy pattern explicit.
    """

    @staticmethod
    def supported_formats() -> list[str]:
        """Return list of supported file extensions.

        Returns:
            List of file extensions (e.g., [".pdf", ".docx", ".pptx", ".xlsx"]).
        """
        return list(EXTRACTOR_MAP.keys())

    def get_extractor(self, file_path: Path | str):
        """Get the appropriate extractor for a file.

        Args:
            file_path: Path or str to the document file.

        Returns:
            Instantiated extractor ready to use (e.g., PDFExtractor).

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is not supported.
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        ext = path.suffix.lower()
        if ext not in EXTRACTOR_MAP:
            supported = ", ".join(EXTRACTOR_MAP.keys())
            raise ValueError(f"Unsupported format: {ext}. Supported: {supported}")

        _, extractor_class = EXTRACTOR_MAP[ext]
        return extractor_class(path)

    def process_document(self, file_path: Path | str) -> ExtractionResult:
        """Process a document and return the extraction result.

        Args:
            file_path: Path or str to the document file.

        Returns:
            ExtractionResult from the appropriate extractor.
        """
        extractor = self.get_extractor(file_path)
        return extractor.extract_all()


def process_document(file_path: Path | str) -> ExtractionResult:
    """Convenience function for one-line document extraction.

    Args:
        file_path: Path or str to the document file.

    Returns:
        ExtractionResult from the appropriate extractor.

    Example:
        result = process_document("path/to/document.pdf")
        print(result.markdown)
    """
    return DocumentRouter().process_document(file_path)
