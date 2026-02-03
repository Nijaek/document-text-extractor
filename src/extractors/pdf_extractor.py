"""
PDF document extractor using PyMuPDF.

This is the most important extractor. PDFs are the most common
document format in enterprise settings and have the most complex
extraction requirements.
"""

import fitz  # pymupdf
from datetime import datetime

# Suppress PyMuPDF's recommendation to install pymupdf_layout package
fitz.no_recommend_layout()

from ..base_extractor import BaseExtractor
from ..models import TableData, ImageData, DocumentMetadata, FileFormat
from ..utils.markdown_helpers import clean_text, heading_to_markdown, normalize_whitespace


class PDFExtractor(BaseExtractor):
    """Extracts content from PDF documents.

    Uses PyMuPDF (fitz) for all extraction operations.
    """

    def __init__(self, file_path) -> None:
        """Initialize PDF extractor.

        Args:
            file_path: Path to PDF file.
        """
        super().__init__(file_path)
        self._doc = fitz.open(self.file_path)

    def extract_text(self) -> str:
        """Extract document text as markdown.

        Returns:
            Clean markdown string with heading hierarchy preserved.
        """
        if len(self._doc) == 0:
            return ""

        # First pass: collect all font sizes to determine heading thresholds
        all_font_sizes = set()
        for page in self._doc:
            text_dict = page.get_text("dict")
            for block in text_dict.get("blocks", []):
                if block.get("type") == 0:  # Text block
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            size = span.get("size", 0)
                            if size > 0:
                                all_font_sizes.add(round(size, 1))

        # Sort font sizes descending to determine heading levels
        sorted_sizes = sorted(all_font_sizes, reverse=True)

        # Map font sizes to heading levels (top 3 distinct sizes)
        size_to_level = {}
        for i, size in enumerate(sorted_sizes[:3]):
            size_to_level[size] = i + 1  # H1, H2, H3

        # Second pass: extract text with heading detection
        lines = []
        for page in self._doc:
            text_dict = page.get_text("dict")
            for block in text_dict.get("blocks", []):
                if block.get("type") == 0:  # Text block
                    block_text = []
                    block_size = None

                    for line in block.get("lines", []):
                        line_text = []
                        for span in line.get("spans", []):
                            text = span.get("text", "").strip()
                            if text:
                                line_text.append(text)
                                # Use the first span's size for the block
                                if block_size is None:
                                    block_size = round(span.get("size", 0), 1)
                        if line_text:
                            block_text.append(" ".join(line_text))

                    if block_text:
                        text = " ".join(block_text)
                        level = size_to_level.get(block_size)
                        if level:
                            lines.append(heading_to_markdown(text, level))
                        else:
                            lines.append(text)

        result = "\n\n".join(lines)
        return normalize_whitespace(clean_text(result))

    def extract_tables(self) -> list[TableData]:
        """Extract all tables from the PDF.

        Returns:
            List of TableData objects.
        """
        tables = []
        for page_num, page in enumerate(self._doc, start=1):
            try:
                page_tables = page.find_tables()
                for table in page_tables:
                    content = []
                    for row in table.extract():
                        # Replace None cells with empty string
                        content.append([cell if cell else "" for cell in row])
                    if content:  # Only add non-empty tables
                        tables.append(TableData(
                            content=content,
                            page_or_slide=page_num
                        ))
            except Exception:
                # Skip pages where table detection fails
                continue
        return tables

    def extract_images(self) -> list[ImageData]:
        """Extract metadata for all images.

        Returns:
            List of ImageData objects.
        """
        images = []
        for page_num, page in enumerate(self._doc, start=1):
            for img_index, img in enumerate(page.get_images(full=True)):
                try:
                    xref = img[0]
                    base_image = self._doc.extract_image(xref)
                    images.append(ImageData(
                        filename=f"image_p{page_num}_i{img_index}.{base_image['ext']}",
                        format=base_image['ext'],
                        width=base_image.get('width'),
                        height=base_image.get('height'),
                        page_or_slide=page_num
                    ))
                except Exception:
                    # Skip corrupt images
                    continue
        return images

    def extract_metadata(self) -> DocumentMetadata:
        """Extract document metadata.

        Returns:
            DocumentMetadata object.
        """
        meta = self._doc.metadata or {}
        return DocumentMetadata(
            title=meta.get('title') or None,
            author=meta.get('author') or None,
            created_date=self._parse_pdf_date(meta.get('creationDate')),
            modified_date=self._parse_pdf_date(meta.get('modDate')),
            page_count=len(self._doc),
            file_format=FileFormat.PDF,
            file_size_bytes=self.file_path.stat().st_size,
            source_filename=self.file_path.name
        )

    def _parse_pdf_date(self, date_str: str | None) -> datetime | None:
        """Parse PDF date string to datetime.

        Args:
            date_str: PDF date format like "D:20240115120000"

        Returns:
            datetime object or None if parsing fails.
        """
        if not date_str:
            return None
        try:
            # Format: D:YYYYMMDDHHmmSS with optional timezone
            cleaned = date_str.replace("D:", "")[:14]
            return datetime.strptime(cleaned, "%Y%m%d%H%M%S")
        except Exception:
            return None
