"""Test shared URL normalization utilities."""

from flowscout.core.url_utils import (
    extract_hostname,
    extract_netloc,
    extract_path,
    extract_path_tail,
    extract_url_path_pattern,
    is_same_origin,
    sanitize_for_filesystem,
)


class TestExtractHostname:
    def test_basic(self) -> None:
        assert extract_hostname("https://example.com/path") == "example.com"

    def test_with_port(self) -> None:
        assert extract_hostname("http://localhost:8080/foo") == "localhost"

    def test_empty(self) -> None:
        assert extract_hostname("") == ""

    def test_no_scheme(self) -> None:
        # urlparse treats schemeless URLs oddly
        assert extract_hostname("example.com") == ""

    def test_uppercase(self) -> None:
        assert extract_hostname("https://EXAMPLE.COM") == "example.com"


class TestExtractNetloc:
    def test_basic(self) -> None:
        assert extract_netloc("https://example.com/path") == "example.com"

    def test_with_port(self) -> None:
        assert extract_netloc("http://localhost:3000") == "localhost:3000"


class TestExtractPath:
    def test_basic(self) -> None:
        assert extract_path("https://example.com/items/42") == "/items/42"

    def test_strips_trailing_slash(self) -> None:
        assert extract_path("https://example.com/items/") == "/items"

    def test_root(self) -> None:
        assert extract_path("https://example.com/") == "/"

    def test_root_no_trailing_slash(self) -> None:
        assert extract_path("https://example.com") == "/"


class TestExtractPathTail:
    def test_basic(self) -> None:
        assert extract_path_tail("https://example.com/items/42") == "42"

    def test_single_segment(self) -> None:
        assert extract_path_tail("https://example.com/about") == "about"

    def test_root(self) -> None:
        assert extract_path_tail("https://example.com/") == ""


class TestExtractUrlPathPattern:
    def test_extracts_path(self) -> None:
        result = extract_url_path_pattern("https://example.com/items/42")
        assert "/items/42" in result

    def test_root_url(self) -> None:
        result = extract_url_path_pattern("https://example.com/")
        assert result  # Should return something

    def test_no_scheme(self) -> None:
        result = extract_url_path_pattern("/local/path")
        assert result == "/local/path"


class TestIsSameOrigin:
    def test_same_origin(self) -> None:
        assert is_same_origin("https://example.com/a", "https://example.com/b")

    def test_different_origin(self) -> None:
        assert not is_same_origin("https://a.com/x", "https://b.com/y")

    def test_empty_base_url(self) -> None:
        assert is_same_origin("https://example.com/a", "")

    def test_different_port(self) -> None:
        assert not is_same_origin(
            "http://localhost:3000", "http://localhost:8080"
        )


class TestSanitizeForFilesystem:
    def test_basic(self) -> None:
        assert sanitize_for_filesystem("example.com") == "example.com"

    def test_port(self) -> None:
        assert sanitize_for_filesystem("localhost:3000") == "localhost_3000"

    def test_special_chars(self) -> None:
        assert sanitize_for_filesystem("a/b?c=d") == "a_b_c_d"

    def test_preserves_hyphens_and_dots(self) -> None:
        assert sanitize_for_filesystem("my-site.example.com") == "my-site.example.com"
