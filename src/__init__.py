"""
Document Extraction System - Main Package

This package provides a unified interface for extracting content from
PDF, DOCX, PPTX, and XLSX documents.

Exports:
    DocumentRouter: Routes files to appropriate extractors
    process_document: Convenience function for one-line extraction
    ExtractionResult: Unified output model from all extractors
    FileFormat: Enum of supported file formats
"""

from .router import DocumentRouter, process_document
from .models import ExtractionResult, FileFormat

__all__ = ["DocumentRouter", "process_document", "ExtractionResult", "FileFormat"]
