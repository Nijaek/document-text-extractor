"""
Document extractors package.

Exports all extractor classes for easy importing.

Usage:
    from src.extractors import PDFExtractor, DOCXExtractor, PPTXExtractor, XLSXExtractor
"""

from .pdf_extractor import PDFExtractor
from .docx_extractor import DOCXExtractor
from .pptx_extractor import PPTXExtractor
from .xlsx_extractor import XLSXExtractor

__all__ = ["PDFExtractor", "DOCXExtractor", "PPTXExtractor", "XLSXExtractor"]
