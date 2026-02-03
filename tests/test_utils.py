"""
Tests for utility functions.
"""

import pytest

from src.utils.markdown_helpers import (
    clean_text,
    heading_to_markdown,
    bold,
    italic,
    normalize_whitespace,
    table_to_json,
)
from src.models import TableData


class TestCleanText:
    """Tests for clean_text function."""

    def test_strips_leading_trailing_whitespace(self):
        """Test clean_text strips leading/trailing whitespace."""
        assert clean_text("  hello  ") == "hello"

    def test_removes_null_characters(self):
        """Test clean_text removes null characters."""
        result = clean_text("hello\x00world")
        assert "\x00" not in result
        assert result == "helloworld"

    def test_normalizes_line_endings(self):
        """Test clean_text normalizes \\r\\n to \\n."""
        result = clean_text("hello\r\nworld")
        assert "\r" not in result
        assert "\n" in result
        assert result == "hello\nworld"

    def test_handles_standalone_carriage_return(self):
        """Test clean_text handles standalone \\r."""
        result = clean_text("hello\rworld")
        assert "\r" not in result
        assert result == "hello\nworld"


class TestHeadingToMarkdown:
    """Tests for heading_to_markdown function."""

    def test_level_1_heading(self):
        """Test heading_to_markdown creates H1."""
        assert heading_to_markdown("Title", 1) == "# Title"

    def test_level_2_heading(self):
        """Test heading_to_markdown creates H2."""
        assert heading_to_markdown("Section", 2) == "## Section"

    def test_level_3_heading(self):
        """Test heading_to_markdown creates H3."""
        assert heading_to_markdown("Subsection", 3) == "### Subsection"

    def test_level_4_heading(self):
        """Test heading_to_markdown creates H4."""
        assert heading_to_markdown("Sub-subsection", 4) == "#### Sub-subsection"

    def test_clamps_level_to_max_6(self):
        """Test heading_to_markdown clamps level to max 6."""
        result = heading_to_markdown("Test", 10)
        assert result.startswith("######")
        assert result == "###### Test"

    def test_clamps_level_to_min_1(self):
        """Test heading_to_markdown clamps level to min 1."""
        result = heading_to_markdown("Test", 0)
        assert result == "# Test"

    def test_strips_heading_text(self):
        """Test heading_to_markdown strips whitespace from text."""
        assert heading_to_markdown("  Title  ", 1) == "# Title"


class TestBold:
    """Tests for bold function."""

    def test_wraps_text(self):
        """Test bold wraps text in **."""
        assert bold("text") == "**text**"

    def test_empty_string(self):
        """Test bold handles empty string."""
        assert bold("") == "****"


class TestItalic:
    """Tests for italic function."""

    def test_wraps_text(self):
        """Test italic wraps text in *."""
        assert italic("text") == "*text*"

    def test_empty_string(self):
        """Test italic handles empty string."""
        assert italic("") == "**"


class TestNormalizeWhitespace:
    """Tests for normalize_whitespace function."""

    def test_collapses_multiple_blank_lines(self):
        """Test normalize_whitespace collapses 3+ newlines to 2."""
        assert normalize_whitespace("a\n\n\n\nb") == "a\n\nb"

    def test_preserves_double_newline(self):
        """Test normalize_whitespace preserves double newlines."""
        assert normalize_whitespace("a\n\nb") == "a\n\nb"

    def test_collapses_many_newlines(self):
        """Test normalize_whitespace handles many newlines."""
        assert normalize_whitespace("a\n\n\n\n\n\nb") == "a\n\nb"


class TestTableToJson:
    """Tests for table_to_json function."""

    def test_extracts_headers(self):
        """Test table_to_json extracts first row as headers."""
        table = TableData(content=[["a", "b"], ["c", "d"]])
        result = table_to_json(table)
        assert result["headers"] == ["a", "b"]

    def test_extracts_rows(self):
        """Test table_to_json extracts remaining rows."""
        table = TableData(content=[["a", "b"], ["c", "d"], ["e", "f"]])
        result = table_to_json(table)
        assert result["rows"] == [["c", "d"], ["e", "f"]]

    def test_empty_table(self):
        """Test table_to_json handles empty table."""
        table = TableData(content=[])
        result = table_to_json(table)
        assert result["headers"] == []
        assert result["rows"] == []

    def test_single_row_table(self):
        """Test table_to_json handles single row (headers only)."""
        table = TableData(content=[["a", "b"]])
        result = table_to_json(table)
        assert result["headers"] == ["a", "b"]
        assert result["rows"] == []
