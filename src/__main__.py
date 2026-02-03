"""
CLI entry point for document extraction.

Usage:
    python -m src <input_file> [-o <output_file>]

Examples:
    python -m src report.pdf
    # Creates report_extracted.json

    python -m src report.pdf -o results.json
    # Creates results.json
"""

import argparse
import sys
from pathlib import Path

from .router import DocumentRouter


def main() -> int:
    """Main CLI entry point.

    Returns:
        Exit code: 0 on success, 1 on error.
    """
    parser = argparse.ArgumentParser(
        prog="document-extractor",
        description="Extract text, tables, and images from documents.",
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Document to process (.pdf, .docx, .pptx, .xlsx)",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output JSON file (default: <input>_extracted.json)",
    )
    args = parser.parse_args()

    # Validate input file exists
    if not args.input_file.exists():
        print(f"Error: File not found: {args.input_file}", file=sys.stderr)
        return 1

    # Determine output path
    output_path = args.output or args.input_file.with_name(
        f"{args.input_file.stem}_extracted.json"
    )

    # Process document
    router = DocumentRouter()
    try:
        result = router.process_document(args.input_file)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Write output
    output_path.write_text(result.model_dump_json(indent=2))
    print(f"Extracted to: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
