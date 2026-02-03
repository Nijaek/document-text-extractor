# Known Limitations

## Current Limitations

| Limitation | Impact | Proposed Solution |
|------------|--------|-------------------|
| No OCR for scanned PDFs | Cannot extract text from image-only PDFs | Integrate Tesseract for local OCR or AWS Textract/Google Document AI for cloud-based OCR |
| DOCX extractor not implemented | Cannot process Word files | Architecture fully supports it — follows same BaseExtractor pattern. Stub included. |
| PPTX extractor not implemented | Cannot process PowerPoint files | Architecture fully supports it — follows same BaseExtractor pattern. Stub included. |
| XLSX extractor not implemented | Cannot process Excel files | Architecture fully supports it — follows same BaseExtractor pattern. Stub included. |
| No AI-powered image descriptions | Only metadata extracted, no semantic content | Integrate a vision model (Claude, GPT-4V) for automatic captioning. Requires API key and cost management. |
| Complex/merged table cells | May produce incorrect cell alignment in some PDFs | Evaluate Camelot or table-detection ML models for higher accuracy on complex layouts |
| No password-protected file support | Encrypted documents fail immediately | Add password parameter to extractors; use pymupdf's decryption for PDF |
| No streaming for large documents | Memory issues on 100+ page documents | Implement page-by-page generator pattern for memory-efficient processing |
| No multi-language testing | Possible encoding issues with non-English documents | Add encoding detection (chardet) and test with diverse language samples |
| Format detection by extension only | Misnamed files route to wrong extractor | Add python-magic or file signature detection as fallback |
| DOCX page count unavailable | Metadata incomplete for DOCX files | Would require rendering the document or using alternative library |

## Future Enhancements

### Multi-File Output Mode

Current CLI outputs a single JSON file. A future `--output-dir` flag would write separate files for different consumers:

```
output/
├── quarterly_report.md          ← clean markdown for human review
├── quarterly_report_tables.json ← tables as JSON for data pipelines
├── quarterly_report_images/     ← extracted image files
│   ├── image_p1_i0.png
│   └── image_p3_i1.jpg
└── quarterly_report_meta.json   ← document metadata
```

This separates concerns: markdown goes to reviewers, JSON feeds downstream systems, images are available for multimodal processing.

### Other Enhancements

- **FastAPI Wrapper**: HTTP API for web service usage
- **Batch Processing**: Async support for processing multiple documents
- **Confidence Scoring**: Quality metrics for extraction results (e.g., OCR confidence, table detection confidence)
- **Incremental Extraction**: Re-extract only changed pages for large documents
