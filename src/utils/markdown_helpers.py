"""
Utility functions for markdown text processing.

Shared across all extractors for consistent text handling.
"""

import re
from ..models import TableData


def clean_text(text: str) -> str:
    """Strip excessive whitespace and normalize line endings.

    Args:
        text: Raw text to clean.

    Returns:
        Cleaned text with normalized whitespace.
    """
    text = text.replace('\x00', '')      # Remove null characters
    text = text.replace('\r\n', '\n')    # Normalize line endings
    text = text.replace('\r', '\n')      # Handle standalone \r
    text = text.strip()                   # Strip leading/trailing whitespace
    return text


def heading_to_markdown(text: str, level: int) -> str:
    """Convert text to a markdown heading.

    Args:
        text: Heading text content.
        level: Heading level (1-6).

    Returns:
        Markdown heading string (e.g., "## My Heading").
    """
    level = max(1, min(6, level))        # Clamp to 1-6
    return '#' * level + ' ' + text.strip()


def bold(text: str) -> str:
    """Wrap text in markdown bold syntax.

    Args:
        text: Text to make bold.

    Returns:
        Text wrapped in ** markers.
    """
    return f'**{text}**'


def italic(text: str) -> str:
    """Wrap text in markdown italic syntax.

    Args:
        text: Text to make italic.

    Returns:
        Text wrapped in * markers.
    """
    return f'*{text}*'


def normalize_whitespace(text: str) -> str:
    """Collapse multiple blank lines to maximum of two.

    Args:
        text: Text with potentially excessive blank lines.

    Returns:
        Text with normalized blank lines.
    """
    return re.sub(r'\n{3,}', '\n\n', text)


def table_to_json(table: TableData) -> dict:
    """Convert TableData to a dict with headers and rows.

    Args:
        table: TableData object to convert.

    Returns:
        Dict with 'headers' (first row) and 'rows' (remaining rows).
    """
    if not table.content:
        return {'headers': [], 'rows': []}
    return {
        'headers': table.content[0],
        'rows': table.content[1:]
    }
