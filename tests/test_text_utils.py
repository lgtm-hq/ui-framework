"""Test shared text normalization utilities."""

from flowscout.core.text_utils import (
    CSS_BLOCK_RE,
    BRACE_RE,
    WHITESPACE_RE,
    normalize_whitespace,
    strip_css_blocks,
)


class TestNormalizeWhitespace:
    def test_collapses_spaces(self) -> None:
        assert normalize_whitespace("hello   world") == "hello world"

    def test_collapses_tabs_and_newlines(self) -> None:
        assert normalize_whitespace("hello\t\n world") == "hello world"

    def test_strips(self) -> None:
        assert normalize_whitespace("  hello  ") == "hello"

    def test_empty(self) -> None:
        assert normalize_whitespace("") == ""


class TestStripCssBlocks:
    def test_removes_css_declarations(self) -> None:
        text = "Hello .btn:hover { color: red; } World"
        assert strip_css_blocks(text) == "Hello World"

    def test_removes_brace_groups(self) -> None:
        text = "Label {content: 'x'} Text"
        assert strip_css_blocks(text) == "Label Text"

    def test_preserves_plain_text(self) -> None:
        assert strip_css_blocks("Just plain text") == "Just plain text"

    def test_normalizes_whitespace(self) -> None:
        assert strip_css_blocks("Hello   World") == "Hello World"

    def test_empty(self) -> None:
        assert strip_css_blocks("") == ""

    def test_complex_css_noise(self) -> None:
        text = "Submit .form-btn:active { opacity: 0.5 } .icon { display: none } Button"
        result = strip_css_blocks(text)
        assert "Submit" in result
        assert "Button" in result
        assert "{" not in result


class TestCompiledPatterns:
    def test_css_block_re_matches(self) -> None:
        assert CSS_BLOCK_RE.search(".btn { color: red; }")

    def test_css_block_re_pseudo(self) -> None:
        assert CSS_BLOCK_RE.search(".btn:hover { opacity: 0.5 }")

    def test_brace_re_matches(self) -> None:
        assert BRACE_RE.search("{anything}")

    def test_whitespace_re_matches(self) -> None:
        assert WHITESPACE_RE.search("  ")
