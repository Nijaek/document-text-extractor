# Known Limitations

<!-- TODO: Frame each limitation with what it is, why it matters, and how to fix it -->

## Current Limitations

| Limitation | Impact | Proposed Solution |
|------------|--------|-------------------|
| No OCR for scanned PDFs | Cannot extract text from image-only PDFs | <!-- TODO: Describe solution --> |
| PPTX extractor not implemented | Cannot process PowerPoint files | <!-- TODO: Describe solution --> |
| No AI-powered image descriptions | Only metadata extracted | <!-- TODO: Describe solution --> |
| Complex/merged table cells | May produce incorrect alignment | <!-- TODO: Describe solution --> |
| No password-protected file support | Encrypted documents fail | <!-- TODO: Describe solution --> |
| No streaming for large documents | Memory issues on large files | <!-- TODO: Describe solution --> |
| No multi-language testing | Possible encoding issues | <!-- TODO: Describe solution --> |
| Format detection by extension only | Misnamed files route incorrectly | <!-- TODO: Describe solution --> |
| DOCX page count unavailable | Incomplete metadata | <!-- TODO: Describe solution --> |

## Future Enhancements

<!-- TODO: Expand on each enhancement -->

- **CLI Interface**: `python -m document_extractor path/to/file.pdf`
- **FastAPI Wrapper**: HTTP API for web service usage
- **Batch Processing**: Async support for multiple documents
- **Output to File**: Write markdown, save images to directory
- **Confidence Scoring**: Quality metrics for extraction results
