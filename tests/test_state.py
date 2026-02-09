"""Tests for page state fingerprinting."""

from flowscout.core.state import (
    ExplorerConfig,
    FingerprintConfig,
    build_fingerprint,
    make_state_id,
    normalize_url,
)


class TestNormalizeUrl:
    def test_strips_trailing_slash(self):
        assert normalize_url("https://example.com/path/") == "https://example.com/path"

    def test_preserves_root_slash(self):
        assert normalize_url("https://example.com/") == "https://example.com/"

    def test_sorts_query_params(self):
        result = normalize_url("https://example.com?b=2&a=1")
        assert "a=1" in result
        assert result.index("a=1") < result.index("b=2")

    def test_strips_fragment(self):
        result = normalize_url("https://example.com/page#section")
        assert "#" not in result

    def test_ignores_specified_params(self):
        result = normalize_url(
            "https://example.com?utm_source=x&page=1",
            ignore_params=["utm_source"],
        )
        assert "utm_source" not in result
        assert "page=1" in result

    def test_allowlist_keeps_only_allowed_params(self):
        result = normalize_url(
            "https://example.com/products?category=shoes&page=2&utm_source=google",
            allow_params=["category", "page"],
        )
        assert "category=shoes" in result
        assert "page=2" in result
        assert "utm_source" not in result

    def test_ignores_wildcard_pattern_params(self):
        result = normalize_url(
            "https://example.com?utm_source=x&fbclid=123&page=1",
            ignore_param_patterns=["utm_*", "fbclid"],
        )
        assert "utm_source" not in result
        assert "fbclid" not in result
        assert "page=1" in result


class TestBuildFingerprint:
    def test_deterministic(self):
        args = {
            "url": "https://example.com",
            "title": "Example",
            "dom_structure_hash": "abc123",
            "visible_text_hash": "def456",
            "form_state_hash": "ghi789",
        }
        fp1 = build_fingerprint(**args)
        fp2 = build_fingerprint(**args)
        assert fp1 == fp2

    def test_different_url_different_fingerprint(self):
        common = {
            "title": "Example",
            "dom_structure_hash": "abc123",
            "visible_text_hash": "def456",
            "form_state_hash": "ghi789",
        }
        fp1 = build_fingerprint(url="https://example.com/a", **common)
        fp2 = build_fingerprint(url="https://example.com/b", **common)
        assert fp1 != fp2

    def test_different_dom_different_fingerprint(self):
        common = {
            "url": "https://example.com",
            "title": "Example",
            "visible_text_hash": "def456",
            "form_state_hash": "ghi789",
        }
        fp1 = build_fingerprint(dom_structure_hash="hash_a", **common)
        fp2 = build_fingerprint(dom_structure_hash="hash_b", **common)
        assert fp1 != fp2

    def test_sha256_hex_format(self):
        fp = build_fingerprint(
            url="https://example.com",
            title="Test",
            dom_structure_hash="a",
            visible_text_hash="b",
            form_state_hash="c",
        )
        assert len(fp) == 64  # SHA-256 hex length

    def test_config_disables_url(self):
        config = FingerprintConfig(include_url=False)
        common = {
            "title": "Example",
            "dom_structure_hash": "abc",
            "visible_text_hash": "def",
            "form_state_hash": "ghi",
        }
        fp1 = build_fingerprint(url="https://a.com", config=config, **common)
        fp2 = build_fingerprint(url="https://b.com", config=config, **common)
        assert fp1 == fp2  # URL ignored


class TestMakeStateId:
    def test_returns_12_chars(self):
        fp = "a" * 64
        assert len(make_state_id(fp)) == 12

    def test_is_prefix_of_fingerprint(self):
        fp = "abcdef1234567890" * 4
        assert make_state_id(fp) == fp[:12]


class TestExplorerConfig:
    def test_non_destructive_policy_enabled_by_default(self):
        config = ExplorerConfig(start_url="https://example.com")
        assert config.action_policy.enforce_non_destructive is True
        assert config.action_policy.block_form_submissions is True
