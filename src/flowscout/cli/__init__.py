"""CLI package for flowscout.

Re-exports public API and internal helpers used by tests.
"""

from __future__ import annotations

# Import main group first, then commands to register them
from flowscout.cli.app import main

# Import command modules to register them with the Click group
import flowscout.cli.benchmark as _benchmark_mod  # noqa: F401
import flowscout.cli.explore as _explore_mod  # noqa: F401
import flowscout.cli.generate as _generate_mod  # noqa: F401
import flowscout.cli.history as _history_mod  # noqa: F401
import flowscout.cli.model as _model_mod  # noqa: F401
import flowscout.cli.reliability as _reliability_mod  # noqa: F401
import flowscout.cli.serve as _serve_mod  # noqa: F401

# Re-export config helpers used by tests
from flowscout.cli.config import (
    CrawlConfig,
    _domain_match_score,
    _load_crawl_config,
    _resolve_auth_bootstrap,
    _resolve_bool_config,
    _resolve_bool_option,
    _resolve_domain_scoped_config,
    _resolve_int_config,
    _resolve_int_option,
    _resolve_str_option,
    validate_crawl_config,
)

# Re-export explore helpers used by tests
from flowscout.cli.explore import _build_output_dirs

# Re-export benchmark helpers used by tests
from flowscout.cli.benchmark import (
    _compute_benchmark_metrics,
    _evaluate_benchmark_gates,
)

__all__ = [
    "CrawlConfig",
    "main",
    "validate_crawl_config",
    "_build_output_dirs",
    "_compute_benchmark_metrics",
    "_domain_match_score",
    "_evaluate_benchmark_gates",
    "_load_crawl_config",
    "_resolve_auth_bootstrap",
    "_resolve_bool_config",
    "_resolve_bool_option",
    "_resolve_domain_scoped_config",
    "_resolve_int_config",
    "_resolve_int_option",
    "_resolve_str_option",
]
