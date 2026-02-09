# Lintro Report

## Summary

| Tool | Issues |
|------|--------|
| black | 2456 |
| sqlfluff | 0 |
| markdownlint | 1 |
| clippy | 0 |
| oxfmt | 2 |
| prettier | 40 |
| actionlint | 0 |
| semgrep | 6 |
| astro-check | 0 |
| svelte-check | 0 |
| gitleaks | 44 |
| mypy | 0 |
| vue-tsc | 0 |
| shellcheck | 0 |
| bandit | 543 |
| shfmt | 0 |
| ruff | 69 |
| oxlint | 6 |
| cargo_deny | 0 |
| yamllint | 0 |
| rustfmt | 0 |
| tsc | 216 |
| hadolint | 0 |
| taplo | 1 |
| pydoclint | 0 |
| cargo_audit | 0 |

### black (2456 issues)
| File | Line | Code | Message |
|------|------|------|---------|
| reports/debs-obrien.github.io/baseline/pages/landing_page.py | 0 |  | Would reformat file |
| reports/2026/02.February/07-02-2026/22.29.41/pom_tests.py | 0 |  | Would reformat file |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/pom_tests.py | 0 |  | Would reformat file |
| reports/2026/02.February/07-02-2026/22.29.41/scenario_tests.py | 0 |  | Would reformat file |
| reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 0 |  | Would reformat file |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/tests.py | 0 |  | Would reformat file |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/pom_tests.py | 0 |  | Would reformat file |
| reports/debs-obrien.github.io/baseline/scenario_tests.py | 0 |  | Would reformat file |
| reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 0 |  | Would reformat file |
| src/flowscout/analysis/expectations.py | 0 |  | Would reformat file |
| src/flowscout/analysis/archetype.py | 0 |  | Would reformat file |
| reports/2026/02.February/07-02-2026/22.29.41/tests.py | 0 |  | Would reformat file |
| src/flowscout/analysis/site_model.py | 0 |  | Would reformat file |
| src/flowscout/core/browser.py | 0 |  | Would reformat file |
| src/flowscout/codegen/pom_tests.py | 0 |  | Would reformat file |
| src/flowscout/codegen/page_objects.py | 0 |  | Would reformat file |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 0 |  | Would reformat file |
| src/flowscout/reporting/html.py | 0 |  | Would reformat file |
| tests/test_actions.py | 0 |  | Would reformat file |
| src/flowscout/core/state.py | 0 |  | Would reformat file |
| tests/test_context.py | 0 |  | Would reformat file |
| src/flowscout/core/navigator.py | 0 |  | Would reformat file |
| tests/test_integration.py | 0 |  | Would reformat file |
| src/flowscout/storage/db.py | 0 |  | Would reformat file |
| src/flowscout/smart/scenarios.py | 0 |  | Would reformat file |
| src/flowscout/reporting/terminal.py | 0 |  | Would reformat file |
| src/flowscout/discovery/elements.py | 0 |  | Would reformat file |
| tests/test_page_objects.py | 0 |  | Would reformat file |
| tests/test_scenarios.py | 0 |  | Would reformat file |
| src/flowscout/codegen/scenario_tests.py | 0 |  | Would reformat file |
| tests/test_scenario_tests_codegen.py | 0 |  | Would reformat file |
| tests/test_archetype.py | 0 |  | Would reformat file |
| tests/test_planner.py | 0 |  | Would reformat file |
| tests/test_site_model.py | 0 |  | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 31 | E501 | Line 31 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 59 | E501 | Line 59 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 91 | E501 | Line 91 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 115 | E501 | Line 115 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 143 | E501 | Line 143 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 175 | E501 | Line 175 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 203 | E501 | Line 203 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 235 | E501 | Line 235 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 259 | E501 | Line 259 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 287 | E501 | Line 287 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 319 | E501 | Line 319 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 339 | E501 | Line 339 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 363 | E501 | Line 363 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 395 | E501 | Line 395 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 423 | E501 | Line 423 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 455 | E501 | Line 455 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 487 | E501 | Line 487 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 515 | E501 | Line 515 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 547 | E501 | Line 547 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 571 | E501 | Line 571 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 599 | E501 | Line 599 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 635 | E501 | Line 635 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 663 | E501 | Line 663 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 745 | E501 | Line 745 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 811 | E501 | Line 811 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 843 | E501 | Line 843 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 875 | E501 | Line 875 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 924 | E501 | Line 924 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 952 | E501 | Line 952 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 984 | E501 | Line 984 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1008 | E501 | Line 1008 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1036 | E501 | Line 1036 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1072 | E501 | Line 1072 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1100 | E501 | Line 1100 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1182 | E501 | Line 1182 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1248 | E501 | Line 1248 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1280 | E501 | Line 1280 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1312 | E501 | Line 1312 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1378 | E501 | Line 1378 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1410 | E501 | Line 1410 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1438 | E501 | Line 1438 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1470 | E501 | Line 1470 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1498 | E501 | Line 1498 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1526 | E501 | Line 1526 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1558 | E501 | Line 1558 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1590 | E501 | Line 1590 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1664 | E501 | Line 1664 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1696 | E501 | Line 1696 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1728 | E501 | Line 1728 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1794 | E501 | Line 1794 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1818 | E501 | Line 1818 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1846 | E501 | Line 1846 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1866 | E501 | Line 1866 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1894 | E501 | Line 1894 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1922 | E501 | Line 1922 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1946 | E501 | Line 1946 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 1995 | E501 | Line 1995 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 2040 | E501 | Line 2040 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 2068 | E501 | Line 2068 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 2096 | E501 | Line 2096 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 2154 | E501 | Line 2154 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 2178 | E501 | Line 2178 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 2202 | E501 | Line 2202 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 2243 | E501 | Line 2243 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 2274 | E501 | Line 2274 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/12.58.21/tests.py | 2294 | E501 | Line 2294 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 25 | E501 | Line 25 exceeds line length limit (Line too long (91 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 32 | E501 | Line 32 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 33 | E501 | Line 33 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 51 | E501 | Line 51 exceeds line length limit (Line too long (161 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 58 | E501 | Line 58 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 59 | E501 | Line 59 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 72 | E501 | Line 72 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 90 | E501 | Line 90 exceeds line length limit (Line too long (162 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 97 | E501 | Line 97 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 98 | E501 | Line 98 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 111 | E501 | Line 111 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 129 | E501 | Line 129 exceeds line length limit (Line too long (162 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 136 | E501 | Line 136 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 137 | E501 | Line 137 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 150 | E501 | Line 150 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 168 | E501 | Line 168 exceeds line length limit (Line too long (164 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 175 | E501 | Line 175 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 176 | E501 | Line 176 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 189 | E501 | Line 189 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 207 | E501 | Line 207 exceeds line length limit (Line too long (164 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 214 | E501 | Line 214 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 215 | E501 | Line 215 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 228 | E501 | Line 228 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 246 | E501 | Line 246 exceeds line length limit (Line too long (164 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 253 | E501 | Line 253 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 254 | E501 | Line 254 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 267 | E501 | Line 267 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 285 | E501 | Line 285 exceeds line length limit (Line too long (181 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 292 | E501 | Line 292 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 293 | E501 | Line 293 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 305 | E501 | Line 305 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 306 | E501 | Line 306 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 324 | E501 | Line 324 exceeds line length limit (Line too long (181 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 331 | E501 | Line 331 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 332 | E501 | Line 332 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 344 | E501 | Line 344 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 345 | E501 | Line 345 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 363 | E501 | Line 363 exceeds line length limit (Line too long (164 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 370 | E501 | Line 370 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 371 | E501 | Line 371 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 384 | E501 | Line 384 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 402 | E501 | Line 402 exceeds line length limit (Line too long (181 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 409 | E501 | Line 409 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 410 | E501 | Line 410 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 422 | E501 | Line 422 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 423 | E501 | Line 423 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 441 | E501 | Line 441 exceeds line length limit (Line too long (181 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 448 | E501 | Line 448 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 449 | E501 | Line 449 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 461 | E501 | Line 461 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 462 | E501 | Line 462 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 480 | E501 | Line 480 exceeds line length limit (Line too long (164 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 487 | E501 | Line 487 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 488 | E501 | Line 488 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 501 | E501 | Line 501 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 519 | E501 | Line 519 exceeds line length limit (Line too long (162 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 526 | E501 | Line 526 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 527 | E501 | Line 527 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 540 | E501 | Line 540 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 558 | E501 | Line 558 exceeds line length limit (Line too long (164 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 565 | E501 | Line 565 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 566 | E501 | Line 566 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 579 | E501 | Line 579 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 595 | E501 | Line 595 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 606 | E501 | Line 606 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 622 | E501 | Line 622 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 633 | E501 | Line 633 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 650 | E501 | Line 650 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 661 | E501 | Line 661 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 678 | E501 | Line 678 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 689 | E501 | Line 689 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 702 | E501 | Line 702 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 710 | E501 | Line 710 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 721 | E501 | Line 721 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 747 | E501 | Line 747 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 773 | E501 | Line 773 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 799 | E501 | Line 799 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 825 | E501 | Line 825 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 851 | E501 | Line 851 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 877 | E501 | Line 877 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 894 | E501 | Line 894 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 905 | E501 | Line 905 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 922 | E501 | Line 922 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 933 | E501 | Line 933 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 959 | E501 | Line 959 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 976 | E501 | Line 976 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 987 | E501 | Line 987 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 1006 | E501 | Line 1006 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 1017 | E501 | Line 1017 exceeds line length limit (Line too long (171 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 1045 | E501 | Line 1045 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 1071 | E501 | Line 1071 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.18.16/tests.py | 1097 | E501 | Line 1097 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 25 | E501 | Line 25 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 33 | E501 | Line 33 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 46 | E501 | Line 46 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 64 | E501 | Line 64 exceeds line length limit (Line too long (111 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 72 | E501 | Line 72 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 85 | E501 | Line 85 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 103 | E501 | Line 103 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 111 | E501 | Line 111 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 124 | E501 | Line 124 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 142 | E501 | Line 142 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 150 | E501 | Line 150 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 163 | E501 | Line 163 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 181 | E501 | Line 181 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 189 | E501 | Line 189 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 202 | E501 | Line 202 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 220 | E501 | Line 220 exceeds line length limit (Line too long (138 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 228 | E501 | Line 228 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 241 | E501 | Line 241 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 267 | E501 | Line 267 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 280 | E501 | Line 280 exceeds line length limit (Line too long (110 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 306 | E501 | Line 306 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 319 | E501 | Line 319 exceeds line length limit (Line too long (110 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 345 | E501 | Line 345 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 358 | E501 | Line 358 exceeds line length limit (Line too long (118 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 384 | E501 | Line 384 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 397 | E501 | Line 397 exceeds line length limit (Line too long (138 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 423 | E501 | Line 423 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 436 | E501 | Line 436 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 454 | E501 | Line 454 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 462 | E501 | Line 462 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 475 | E501 | Line 475 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 493 | E501 | Line 493 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 501 | E501 | Line 501 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 514 | E501 | Line 514 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 532 | E501 | Line 532 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 540 | E501 | Line 540 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 553 | E501 | Line 553 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 578 | E501 | Line 578 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 606 | E501 | Line 606 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 632 | E501 | Line 632 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 658 | E501 | Line 658 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 671 | E501 | Line 671 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 688 | E501 | Line 688 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 714 | E501 | Line 714 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 740 | E501 | Line 740 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 766 | E501 | Line 766 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 792 | E501 | Line 792 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 818 | E501 | Line 818 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 844 | E501 | Line 844 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 870 | E501 | Line 870 exceeds line length limit (Line too long (110 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 896 | E501 | Line 896 exceeds line length limit (Line too long (110 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 922 | E501 | Line 922 exceeds line length limit (Line too long (118 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 950 | E501 | Line 950 exceeds line length limit (Line too long (138 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 978 | E501 | Line 978 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 1006 | E501 | Line 1006 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 1032 | E501 | Line 1032 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/20.50.18/tests.py | 1058 | E501 | Line 1058 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 25 | E501 | Line 25 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 33 | E501 | Line 33 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 46 | E501 | Line 46 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 64 | E501 | Line 64 exceeds line length limit (Line too long (111 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 72 | E501 | Line 72 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 85 | E501 | Line 85 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 103 | E501 | Line 103 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 111 | E501 | Line 111 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 124 | E501 | Line 124 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 142 | E501 | Line 142 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 150 | E501 | Line 150 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 163 | E501 | Line 163 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 181 | E501 | Line 181 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 189 | E501 | Line 189 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 202 | E501 | Line 202 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 220 | E501 | Line 220 exceeds line length limit (Line too long (138 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 228 | E501 | Line 228 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 241 | E501 | Line 241 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 267 | E501 | Line 267 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 280 | E501 | Line 280 exceeds line length limit (Line too long (110 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 306 | E501 | Line 306 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 319 | E501 | Line 319 exceeds line length limit (Line too long (110 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 345 | E501 | Line 345 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 358 | E501 | Line 358 exceeds line length limit (Line too long (118 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 384 | E501 | Line 384 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 397 | E501 | Line 397 exceeds line length limit (Line too long (138 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 423 | E501 | Line 423 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 436 | E501 | Line 436 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 454 | E501 | Line 454 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 462 | E501 | Line 462 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 475 | E501 | Line 475 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 493 | E501 | Line 493 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 501 | E501 | Line 501 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 514 | E501 | Line 514 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 532 | E501 | Line 532 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 540 | E501 | Line 540 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 553 | E501 | Line 553 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 578 | E501 | Line 578 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 606 | E501 | Line 606 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 632 | E501 | Line 632 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 658 | E501 | Line 658 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 671 | E501 | Line 671 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 688 | E501 | Line 688 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 714 | E501 | Line 714 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 740 | E501 | Line 740 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 766 | E501 | Line 766 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 792 | E501 | Line 792 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 818 | E501 | Line 818 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 844 | E501 | Line 844 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 870 | E501 | Line 870 exceeds line length limit (Line too long (110 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 896 | E501 | Line 896 exceeds line length limit (Line too long (110 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 922 | E501 | Line 922 exceeds line length limit (Line too long (118 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 950 | E501 | Line 950 exceeds line length limit (Line too long (138 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 978 | E501 | Line 978 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 1006 | E501 | Line 1006 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 1032 | E501 | Line 1032 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.01.27/tests.py | 1058 | E501 | Line 1058 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 26 | E501 | Line 26 exceeds line length limit (Line too long (114 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 34 | E501 | Line 34 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 47 | E501 | Line 47 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 65 | E501 | Line 65 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 73 | E501 | Line 73 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 86 | E501 | Line 86 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 104 | E501 | Line 104 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 112 | E501 | Line 112 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 125 | E501 | Line 125 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 143 | E501 | Line 143 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 151 | E501 | Line 151 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 164 | E501 | Line 164 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 188 | E501 | Line 188 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 201 | E501 | Line 201 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 222 | E501 | Line 222 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 230 | E501 | Line 230 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 243 | E501 | Line 243 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 261 | E501 | Line 261 exceeds line length limit (Line too long (138 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 269 | E501 | Line 269 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 282 | E501 | Line 282 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 308 | E501 | Line 308 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 321 | E501 | Line 321 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 344 | E501 | Line 344 exceeds line length limit (Line too long (136 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 352 | E501 | Line 352 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 365 | E501 | Line 365 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 383 | E501 | Line 383 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 391 | E501 | Line 391 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 404 | E501 | Line 404 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 422 | E501 | Line 422 exceeds line length limit (Line too long (136 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 430 | E501 | Line 430 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 443 | E501 | Line 443 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 461 | E501 | Line 461 exceeds line length limit (Line too long (136 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 469 | E501 | Line 469 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 482 | E501 | Line 482 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 500 | E501 | Line 500 exceeds line length limit (Line too long (137 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 508 | E501 | Line 508 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 521 | E501 | Line 521 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 539 | E501 | Line 539 exceeds line length limit (Line too long (136 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 547 | E501 | Line 547 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 560 | E501 | Line 560 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 578 | E501 | Line 578 exceeds line length limit (Line too long (135 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 586 | E501 | Line 586 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 599 | E501 | Line 599 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 624 | E501 | Line 624 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 652 | E501 | Line 652 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 678 | E501 | Line 678 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 704 | E501 | Line 704 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 717 | E501 | Line 717 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 734 | E501 | Line 734 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 760 | E501 | Line 760 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 786 | E501 | Line 786 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 812 | E501 | Line 812 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 838 | E501 | Line 838 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 867 | E501 | Line 867 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 893 | E501 | Line 893 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 921 | E501 | Line 921 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 952 | E501 | Line 952 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 978 | E501 | Line 978 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 1004 | E501 | Line 1004 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 1030 | E501 | Line 1030 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 1056 | E501 | Line 1056 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 1082 | E501 | Line 1082 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 1108 | E501 | Line 1108 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.02.55/tests.py | 1128 | E501 | Line 1128 exceeds line length limit (Line too long (131 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 25 | E501 | Line 25 exceeds line length limit (Line too long (114 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 33 | E501 | Line 33 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 46 | E501 | Line 46 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 72 | E501 | Line 72 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 95 | E501 | Line 95 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 103 | E501 | Line 103 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 116 | E501 | Line 116 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 134 | E501 | Line 134 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 142 | E501 | Line 142 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 155 | E501 | Line 155 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 173 | E501 | Line 173 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 181 | E501 | Line 181 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 194 | E501 | Line 194 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 218 | E501 | Line 218 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 231 | E501 | Line 231 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 252 | E501 | Line 252 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 260 | E501 | Line 260 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 273 | E501 | Line 273 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 289 | E501 | Line 289 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 299 | E501 | Line 299 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 322 | E501 | Line 322 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 330 | E501 | Line 330 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 343 | E501 | Line 343 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 361 | E501 | Line 361 exceeds line length limit (Line too long (138 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 369 | E501 | Line 369 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 382 | E501 | Line 382 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 408 | E501 | Line 408 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 421 | E501 | Line 421 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 444 | E501 | Line 444 exceeds line length limit (Line too long (136 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 452 | E501 | Line 452 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 465 | E501 | Line 465 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 483 | E501 | Line 483 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 491 | E501 | Line 491 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 504 | E501 | Line 504 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 538 | E501 | Line 538 exceeds line length limit (Line too long (136 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 546 | E501 | Line 546 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 559 | E501 | Line 559 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 584 | E501 | Line 584 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 612 | E501 | Line 612 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 638 | E501 | Line 638 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 664 | E501 | Line 664 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 677 | E501 | Line 677 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 694 | E501 | Line 694 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 720 | E501 | Line 720 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 746 | E501 | Line 746 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 772 | E501 | Line 772 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 798 | E501 | Line 798 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 827 | E501 | Line 827 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 853 | E501 | Line 853 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 879 | E501 | Line 879 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 907 | E501 | Line 907 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 938 | E501 | Line 938 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 964 | E501 | Line 964 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.09.33/tests.py | 990 | E501 | Line 990 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 24 | E501 | Line 24 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 34 | E501 | Line 34 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 60 | E501 | Line 60 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 78 | E501 | Line 78 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 86 | E501 | Line 86 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 99 | E501 | Line 99 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 117 | E501 | Line 117 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 125 | E501 | Line 125 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 138 | E501 | Line 138 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 156 | E501 | Line 156 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 164 | E501 | Line 164 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 177 | E501 | Line 177 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 203 | E501 | Line 203 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 216 | E501 | Line 216 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 247 | E501 | Line 247 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 270 | E501 | Line 270 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 278 | E501 | Line 278 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 296 | E501 | Line 296 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 314 | E501 | Line 314 exceeds line length limit (Line too long (199 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 322 | E501 | Line 322 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 335 | E501 | Line 335 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 348 | E501 | Line 348 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 361 | E501 | Line 361 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 387 | E501 | Line 387 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 400 | E501 | Line 400 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 421 | E501 | Line 421 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 429 | E501 | Line 429 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 447 | E501 | Line 447 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 465 | E501 | Line 465 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 473 | E501 | Line 473 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 486 | E501 | Line 486 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 499 | E501 | Line 499 exceeds line length limit (Line too long (94 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 513 | E501 | Line 513 exceeds line length limit (Line too long (199 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 521 | E501 | Line 521 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 534 | E501 | Line 534 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 547 | E501 | Line 547 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 560 | E501 | Line 560 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 578 | E501 | Line 578 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 586 | E501 | Line 586 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 599 | E501 | Line 599 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 612 | E501 | Line 612 exceeds line length limit (Line too long (94 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 626 | E501 | Line 626 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 634 | E501 | Line 634 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 647 | E501 | Line 647 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 663 | E501 | Line 663 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 681 | E501 | Line 681 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 689 | E501 | Line 689 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 702 | E501 | Line 702 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 718 | E501 | Line 718 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 750 | E501 | Line 750 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 752 | E501 | Line 752 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 760 | E501 | Line 760 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 773 | E501 | Line 773 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 789 | E501 | Line 789 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 815 | E501 | Line 815 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 828 | E501 | Line 828 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 844 | E501 | Line 844 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 860 | E501 | Line 860 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 862 | E501 | Line 862 exceeds line length limit (Line too long (127 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 870 | E501 | Line 870 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 883 | E501 | Line 883 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 899 | E501 | Line 899 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 924 | E501 | Line 924 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 949 | E501 | Line 949 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 975 | E501 | Line 975 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 1001 | E501 | Line 1001 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 1014 | E501 | Line 1014 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 1031 | E501 | Line 1031 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 1059 | E501 | Line 1059 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 1085 | E501 | Line 1085 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 1111 | E501 | Line 1111 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 1137 | E501 | Line 1137 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 1163 | E501 | Line 1163 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 1194 | E501 | Line 1194 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 1223 | E501 | Line 1223 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 1252 | E501 | Line 1252 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 1280 | E501 | Line 1280 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 1308 | E501 | Line 1308 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 1336 | E501 | Line 1336 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 1364 | E501 | Line 1364 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.17.49/tests.py | 1377 | E501 | Line 1377 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 24 | E501 | Line 24 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 34 | E501 | Line 34 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 60 | E501 | Line 60 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 78 | E501 | Line 78 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 86 | E501 | Line 86 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 99 | E501 | Line 99 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 125 | E501 | Line 125 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 138 | E501 | Line 138 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 169 | E501 | Line 169 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 200 | E501 | Line 200 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 213 | E501 | Line 213 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 234 | E501 | Line 234 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 242 | E501 | Line 242 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 255 | E501 | Line 255 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 271 | E501 | Line 271 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 289 | E501 | Line 289 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 297 | E501 | Line 297 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 310 | E501 | Line 310 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 326 | E501 | Line 326 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 342 | E501 | Line 342 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 344 | E501 | Line 344 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 352 | E501 | Line 352 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 365 | E501 | Line 365 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 381 | E501 | Line 381 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 407 | E501 | Line 407 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 420 | E501 | Line 420 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 436 | E501 | Line 436 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 452 | E501 | Line 452 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 454 | E501 | Line 454 exceeds line length limit (Line too long (127 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 462 | E501 | Line 462 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 475 | E501 | Line 475 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 491 | E501 | Line 491 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 522 | E501 | Line 522 exceeds line length limit (Line too long (105 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 540 | E501 | Line 540 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 548 | E501 | Line 548 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 561 | E501 | Line 561 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 577 | E501 | Line 577 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 608 | E501 | Line 608 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 634 | E501 | Line 634 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 647 | E501 | Line 647 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 663 | E501 | Line 663 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 689 | E501 | Line 689 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 702 | E501 | Line 702 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 728 | E501 | Line 728 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 741 | E501 | Line 741 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 766 | E501 | Line 766 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 794 | E501 | Line 794 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 820 | E501 | Line 820 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 846 | E501 | Line 846 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 859 | E501 | Line 859 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 876 | E501 | Line 876 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 904 | E501 | Line 904 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 930 | E501 | Line 930 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 956 | E501 | Line 956 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 982 | E501 | Line 982 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 1008 | E501 | Line 1008 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 1039 | E501 | Line 1039 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 1068 | E501 | Line 1068 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 1097 | E501 | Line 1097 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 1125 | E501 | Line 1125 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 1153 | E501 | Line 1153 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 1181 | E501 | Line 1181 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 1209 | E501 | Line 1209 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 1222 | E501 | Line 1222 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 1239 | E501 | Line 1239 exceeds line length limit (Line too long (105 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 1265 | E501 | Line 1265 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.20.08/tests.py | 1293 | E501 | Line 1293 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 34 | E501 | Line 34 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 52 | E501 | Line 52 exceeds line length limit (Line too long (114 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 60 | E501 | Line 60 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 73 | E501 | Line 73 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 97 | E501 | Line 97 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 110 | E501 | Line 110 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 131 | E501 | Line 131 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 139 | E501 | Line 139 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 152 | E501 | Line 152 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 178 | E501 | Line 178 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 204 | E501 | Line 204 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 217 | E501 | Line 217 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 233 | E501 | Line 233 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 259 | E501 | Line 259 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 272 | E501 | Line 272 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 288 | E501 | Line 288 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 314 | E501 | Line 314 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 327 | E501 | Line 327 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 343 | E501 | Line 343 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 361 | E501 | Line 361 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 369 | E501 | Line 369 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 382 | E501 | Line 382 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 398 | E501 | Line 398 exceeds line length limit (Line too long (136 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 424 | E501 | Line 424 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 437 | E501 | Line 437 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 453 | E501 | Line 453 exceeds line length limit (Line too long (105 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 479 | E501 | Line 479 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 492 | E501 | Line 492 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 508 | E501 | Line 508 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 534 | E501 | Line 534 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 547 | E501 | Line 547 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 563 | E501 | Line 563 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 589 | E501 | Line 589 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 602 | E501 | Line 602 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 618 | E501 | Line 618 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 644 | E501 | Line 644 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 662 | E501 | Line 662 exceeds line length limit (Line too long (114 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 670 | E501 | Line 670 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 683 | E501 | Line 683 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 709 | E501 | Line 709 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 722 | E501 | Line 722 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 748 | E501 | Line 748 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 761 | E501 | Line 761 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 786 | E501 | Line 786 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 814 | E501 | Line 814 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 840 | E501 | Line 840 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 866 | E501 | Line 866 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 879 | E501 | Line 879 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 896 | E501 | Line 896 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 922 | E501 | Line 922 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 948 | E501 | Line 948 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 974 | E501 | Line 974 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 1000 | E501 | Line 1000 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 1029 | E501 | Line 1029 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 1055 | E501 | Line 1055 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 1083 | E501 | Line 1083 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 1109 | E501 | Line 1109 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 1138 | E501 | Line 1138 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 1164 | E501 | Line 1164 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 1190 | E501 | Line 1190 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 1216 | E501 | Line 1216 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 1242 | E501 | Line 1242 exceeds line length limit (Line too long (136 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 1270 | E501 | Line 1270 exceeds line length limit (Line too long (105 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 1296 | E501 | Line 1296 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 1324 | E501 | Line 1324 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 1352 | E501 | Line 1352 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 1378 | E501 | Line 1378 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.23.27/tests.py | 1404 | E501 | Line 1404 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 32 | E501 | Line 32 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 48 | E501 | Line 48 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 50 | E501 | Line 50 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 58 | E501 | Line 58 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 71 | E501 | Line 71 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 87 | E501 | Line 87 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 103 | E501 | Line 103 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 113 | E501 | Line 113 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 131 | E501 | Line 131 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 139 | E501 | Line 139 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 152 | E501 | Line 152 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 170 | E501 | Line 170 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 178 | E501 | Line 178 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 191 | E501 | Line 191 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 209 | E501 | Line 209 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 217 | E501 | Line 217 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 230 | E501 | Line 230 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 248 | E501 | Line 248 exceeds line length limit (Line too long (169 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 256 | E501 | Line 256 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 269 | E501 | Line 269 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 286 | E501 | Line 286 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 287 | E501 | Line 287 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 290 | E501 | Line 290 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 294 | E501 | Line 294 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 308 | E501 | Line 308 exceeds line length limit (Line too long (207 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 316 | E501 | Line 316 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 329 | E501 | Line 329 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 341 | E501 | Line 341 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 342 | E501 | Line 342 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 345 | E501 | Line 345 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 349 | E501 | Line 349 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 363 | E501 | Line 363 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 371 | E501 | Line 371 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 383 | E501 | Line 383 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 384 | E501 | Line 384 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 387 | E501 | Line 387 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 391 | E501 | Line 391 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 405 | E501 | Line 405 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 412 | E501 | Line 412 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 413 | E501 | Line 413 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 416 | E501 | Line 416 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 420 | E501 | Line 420 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 434 | E501 | Line 434 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 442 | E501 | Line 442 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 455 | E501 | Line 455 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 468 | E501 | Line 468 exceeds line length limit (Line too long (94 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 482 | E501 | Line 482 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 490 | E501 | Line 490 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 503 | E501 | Line 503 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 529 | E501 | Line 529 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 542 | E501 | Line 542 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 563 | E501 | Line 563 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 571 | E501 | Line 571 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 584 | E501 | Line 584 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 602 | E501 | Line 602 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 610 | E501 | Line 610 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 623 | E501 | Line 623 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 641 | E501 | Line 641 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 649 | E501 | Line 649 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 662 | E501 | Line 662 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 678 | E501 | Line 678 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 696 | E501 | Line 696 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 704 | E501 | Line 704 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 717 | E501 | Line 717 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 733 | E501 | Line 733 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 751 | E501 | Line 751 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 759 | E501 | Line 759 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 772 | E501 | Line 772 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 788 | E501 | Line 788 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 814 | E501 | Line 814 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 827 | E501 | Line 827 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 843 | E501 | Line 843 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 859 | E501 | Line 859 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 861 | E501 | Line 861 exceeds line length limit (Line too long (127 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 869 | E501 | Line 869 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 882 | E501 | Line 882 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 898 | E501 | Line 898 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 924 | E501 | Line 924 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 937 | E501 | Line 937 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 953 | E501 | Line 953 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 979 | E501 | Line 979 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 992 | E501 | Line 992 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1018 | E501 | Line 1018 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1031 | E501 | Line 1031 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1056 | E501 | Line 1056 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1081 | E501 | Line 1081 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1107 | E501 | Line 1107 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1133 | E501 | Line 1133 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1146 | E501 | Line 1146 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1163 | E501 | Line 1163 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1191 | E501 | Line 1191 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1217 | E501 | Line 1217 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1243 | E501 | Line 1243 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1269 | E501 | Line 1269 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1300 | E501 | Line 1300 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1319 | E501 | Line 1319 exceeds line length limit (Line too long (120 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1330 | E501 | Line 1330 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1333 | E501 | Line 1333 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1337 | E501 | Line 1337 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1359 | E501 | Line 1359 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1387 | E501 | Line 1387 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1416 | E501 | Line 1416 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1442 | E501 | Line 1442 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1468 | E501 | Line 1468 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1497 | E501 | Line 1497 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1523 | E501 | Line 1523 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1551 | E501 | Line 1551 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1579 | E501 | Line 1579 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1607 | E501 | Line 1607 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1635 | E501 | Line 1635 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1648 | E501 | Line 1648 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.25.53/tests.py | 1665 | E501 | Line 1665 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 25 | E501 | Line 25 exceeds line length limit (Line too long (114 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 33 | E501 | Line 33 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 46 | E501 | Line 46 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 64 | E501 | Line 64 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 72 | E501 | Line 72 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 85 | E501 | Line 85 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 103 | E501 | Line 103 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 111 | E501 | Line 111 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 124 | E501 | Line 124 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 142 | E501 | Line 142 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 150 | E501 | Line 150 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 163 | E501 | Line 163 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 187 | E501 | Line 187 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 200 | E501 | Line 200 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 221 | E501 | Line 221 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 229 | E501 | Line 229 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 242 | E501 | Line 242 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 260 | E501 | Line 260 exceeds line length limit (Line too long (144 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 268 | E501 | Line 268 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 280 | E501 | Line 280 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 281 | E501 | Line 281 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 284 | E501 | Line 284 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 288 | E501 | Line 288 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 302 | E501 | Line 302 exceeds line length limit (Line too long (173 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 310 | E501 | Line 310 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 322 | E501 | Line 322 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 323 | E501 | Line 323 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 326 | E501 | Line 326 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 330 | E501 | Line 330 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 344 | E501 | Line 344 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 352 | E501 | Line 352 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 364 | E501 | Line 364 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 365 | E501 | Line 365 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 368 | E501 | Line 368 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 372 | E501 | Line 372 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 386 | E501 | Line 386 exceeds line length limit (Line too long (138 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 394 | E501 | Line 394 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 407 | E501 | Line 407 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 433 | E501 | Line 433 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 446 | E501 | Line 446 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 469 | E501 | Line 469 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 477 | E501 | Line 477 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 490 | E501 | Line 490 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 508 | E501 | Line 508 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 516 | E501 | Line 516 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 529 | E501 | Line 529 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 553 | E501 | Line 553 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 566 | E501 | Line 566 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 587 | E501 | Line 587 exceeds line length limit (Line too long (137 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 595 | E501 | Line 595 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 608 | E501 | Line 608 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 626 | E501 | Line 626 exceeds line length limit (Line too long (136 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 634 | E501 | Line 634 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 647 | E501 | Line 647 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 665 | E501 | Line 665 exceeds line length limit (Line too long (135 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 673 | E501 | Line 673 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 686 | E501 | Line 686 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 704 | E501 | Line 704 exceeds line length limit (Line too long (136 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 712 | E501 | Line 712 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 725 | E501 | Line 725 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 743 | E501 | Line 743 exceeds line length limit (Line too long (108 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 751 | E501 | Line 751 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 764 | E501 | Line 764 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 782 | E501 | Line 782 exceeds line length limit (Line too long (111 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 790 | E501 | Line 790 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 803 | E501 | Line 803 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 821 | E501 | Line 821 exceeds line length limit (Line too long (108 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 829 | E501 | Line 829 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 842 | E501 | Line 842 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 867 | E501 | Line 867 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 895 | E501 | Line 895 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 921 | E501 | Line 921 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 947 | E501 | Line 947 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 960 | E501 | Line 960 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 977 | E501 | Line 977 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1003 | E501 | Line 1003 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1029 | E501 | Line 1029 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1055 | E501 | Line 1055 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1081 | E501 | Line 1081 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1110 | E501 | Line 1110 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1127 | E501 | Line 1127 exceeds line length limit (Line too long (120 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1138 | E501 | Line 1138 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1141 | E501 | Line 1141 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1145 | E501 | Line 1145 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1167 | E501 | Line 1167 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1195 | E501 | Line 1195 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1226 | E501 | Line 1226 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1252 | E501 | Line 1252 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1280 | E501 | Line 1280 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1306 | E501 | Line 1306 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1335 | E501 | Line 1335 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1361 | E501 | Line 1361 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1387 | E501 | Line 1387 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1415 | E501 | Line 1415 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1441 | E501 | Line 1441 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1467 | E501 | Line 1467 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.47.14/tests.py | 1493 | E501 | Line 1493 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 23 | E501 | Line 23 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 33 | E501 | Line 33 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 51 | E501 | Line 51 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 59 | E501 | Line 59 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 72 | E501 | Line 72 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 90 | E501 | Line 90 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 98 | E501 | Line 98 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 111 | E501 | Line 111 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 129 | E501 | Line 129 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 137 | E501 | Line 137 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 150 | E501 | Line 150 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 176 | E501 | Line 176 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 189 | E501 | Line 189 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 212 | E501 | Line 212 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 220 | E501 | Line 220 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 233 | E501 | Line 233 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 251 | E501 | Line 251 exceeds line length limit (Line too long (149 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 259 | E501 | Line 259 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 271 | E501 | Line 271 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 272 | E501 | Line 272 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 275 | E501 | Line 275 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 279 | E501 | Line 279 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 293 | E501 | Line 293 exceeds line length limit (Line too long (144 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 301 | E501 | Line 301 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 313 | E501 | Line 313 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 314 | E501 | Line 314 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 317 | E501 | Line 317 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 321 | E501 | Line 321 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 335 | E501 | Line 335 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 343 | E501 | Line 343 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 355 | E501 | Line 355 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 356 | E501 | Line 356 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 359 | E501 | Line 359 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 363 | E501 | Line 363 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 377 | E501 | Line 377 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 385 | E501 | Line 385 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 398 | E501 | Line 398 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 422 | E501 | Line 422 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 435 | E501 | Line 435 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 456 | E501 | Line 456 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 464 | E501 | Line 464 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 477 | E501 | Line 477 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 503 | E501 | Line 503 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 516 | E501 | Line 516 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 545 | E501 | Line 545 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 558 | E501 | Line 558 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 579 | E501 | Line 579 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 587 | E501 | Line 587 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 600 | E501 | Line 600 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 618 | E501 | Line 618 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 626 | E501 | Line 626 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 639 | E501 | Line 639 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 657 | E501 | Line 657 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 665 | E501 | Line 665 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 678 | E501 | Line 678 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 696 | E501 | Line 696 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 704 | E501 | Line 704 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 717 | E501 | Line 717 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 735 | E501 | Line 735 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 743 | E501 | Line 743 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 756 | E501 | Line 756 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 782 | E501 | Line 782 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 795 | E501 | Line 795 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 822 | E501 | Line 822 exceeds line length limit (Line too long (105 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 840 | E501 | Line 840 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 848 | E501 | Line 848 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 861 | E501 | Line 861 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 886 | E501 | Line 886 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 911 | E501 | Line 911 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 937 | E501 | Line 937 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 963 | E501 | Line 963 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 976 | E501 | Line 976 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 993 | E501 | Line 993 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1021 | E501 | Line 1021 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1047 | E501 | Line 1047 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1073 | E501 | Line 1073 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1099 | E501 | Line 1099 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1130 | E501 | Line 1130 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1149 | E501 | Line 1149 exceeds line length limit (Line too long (120 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1160 | E501 | Line 1160 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1163 | E501 | Line 1163 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1167 | E501 | Line 1167 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1189 | E501 | Line 1189 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1215 | E501 | Line 1215 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1244 | E501 | Line 1244 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1272 | E501 | Line 1272 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1301 | E501 | Line 1301 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1330 | E501 | Line 1330 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1356 | E501 | Line 1356 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1384 | E501 | Line 1384 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1410 | E501 | Line 1410 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1436 | E501 | Line 1436 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1462 | E501 | Line 1462 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1491 | E501 | Line 1491 exceeds line length limit (Line too long (105 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.49.16/tests.py | 1517 | E501 | Line 1517 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 32 | E501 | Line 32 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 48 | E501 | Line 48 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 50 | E501 | Line 50 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 58 | E501 | Line 58 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 71 | E501 | Line 71 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 87 | E501 | Line 87 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 103 | E501 | Line 103 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 105 | E501 | Line 105 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 113 | E501 | Line 113 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 126 | E501 | Line 126 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 142 | E501 | Line 142 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 158 | E501 | Line 158 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 168 | E501 | Line 168 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 186 | E501 | Line 186 exceeds line length limit (Line too long (214 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 194 | E501 | Line 194 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 207 | E501 | Line 207 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 219 | E501 | Line 219 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 220 | E501 | Line 220 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 223 | E501 | Line 223 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 227 | E501 | Line 227 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 241 | E501 | Line 241 exceeds line length limit (Line too long (163 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 249 | E501 | Line 249 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 262 | E501 | Line 262 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 277 | E501 | Line 277 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 278 | E501 | Line 278 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 281 | E501 | Line 281 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 285 | E501 | Line 285 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 299 | E501 | Line 299 exceeds line length limit (Line too long (135 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 307 | E501 | Line 307 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 319 | E501 | Line 319 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 320 | E501 | Line 320 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 323 | E501 | Line 323 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 327 | E501 | Line 327 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 341 | E501 | Line 341 exceeds line length limit (Line too long (208 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 349 | E501 | Line 349 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 362 | E501 | Line 362 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 374 | E501 | Line 374 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 375 | E501 | Line 375 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 378 | E501 | Line 378 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 382 | E501 | Line 382 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 396 | E501 | Line 396 exceeds line length limit (Line too long (207 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 404 | E501 | Line 404 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 417 | E501 | Line 417 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 429 | E501 | Line 429 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 430 | E501 | Line 430 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 433 | E501 | Line 433 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 437 | E501 | Line 437 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 451 | E501 | Line 451 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 459 | E501 | Line 459 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 471 | E501 | Line 471 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 472 | E501 | Line 472 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 475 | E501 | Line 475 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 479 | E501 | Line 479 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 493 | E501 | Line 493 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 500 | E501 | Line 500 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 501 | E501 | Line 501 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 504 | E501 | Line 504 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 508 | E501 | Line 508 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 530 | E501 | Line 530 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 543 | E501 | Line 543 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 566 | E501 | Line 566 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 574 | E501 | Line 574 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 587 | E501 | Line 587 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 605 | E501 | Line 605 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 613 | E501 | Line 613 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 626 | E501 | Line 626 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 652 | E501 | Line 652 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 665 | E501 | Line 665 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 681 | E501 | Line 681 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 697 | E501 | Line 697 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 699 | E501 | Line 699 exceeds line length limit (Line too long (127 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 707 | E501 | Line 707 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 720 | E501 | Line 720 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 736 | E501 | Line 736 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 762 | E501 | Line 762 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 775 | E501 | Line 775 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 791 | E501 | Line 791 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 809 | E501 | Line 809 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 817 | E501 | Line 817 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 830 | E501 | Line 830 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 846 | E501 | Line 846 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 864 | E501 | Line 864 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 872 | E501 | Line 872 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 885 | E501 | Line 885 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 901 | E501 | Line 901 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 919 | E501 | Line 919 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 927 | E501 | Line 927 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 940 | E501 | Line 940 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 956 | E501 | Line 956 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 982 | E501 | Line 982 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 995 | E501 | Line 995 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1011 | E501 | Line 1011 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1037 | E501 | Line 1037 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1050 | E501 | Line 1050 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1066 | E501 | Line 1066 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1084 | E501 | Line 1084 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1092 | E501 | Line 1092 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1105 | E501 | Line 1105 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1121 | E501 | Line 1121 exceeds line length limit (Line too long (122 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1139 | E501 | Line 1139 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1147 | E501 | Line 1147 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1160 | E501 | Line 1160 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1176 | E501 | Line 1176 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1202 | E501 | Line 1202 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1215 | E501 | Line 1215 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1231 | E501 | Line 1231 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1249 | E501 | Line 1249 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1257 | E501 | Line 1257 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1270 | E501 | Line 1270 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1286 | E501 | Line 1286 exceeds line length limit (Line too long (129 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1312 | E501 | Line 1312 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1325 | E501 | Line 1325 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1341 | E501 | Line 1341 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1367 | E501 | Line 1367 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1380 | E501 | Line 1380 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1406 | E501 | Line 1406 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1419 | E501 | Line 1419 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1445 | E501 | Line 1445 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1458 | E501 | Line 1458 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1484 | E501 | Line 1484 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1500 | E501 | Line 1500 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1525 | E501 | Line 1525 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1550 | E501 | Line 1550 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1576 | E501 | Line 1576 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1602 | E501 | Line 1602 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1615 | E501 | Line 1615 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1632 | E501 | Line 1632 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1651 | E501 | Line 1651 exceeds line length limit (Line too long (120 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1662 | E501 | Line 1662 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1665 | E501 | Line 1665 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1669 | E501 | Line 1669 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1691 | E501 | Line 1691 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1717 | E501 | Line 1717 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1743 | E501 | Line 1743 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1769 | E501 | Line 1769 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1800 | E501 | Line 1800 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1828 | E501 | Line 1828 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1856 | E501 | Line 1856 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1885 | E501 | Line 1885 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1914 | E501 | Line 1914 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1940 | E501 | Line 1940 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1966 | E501 | Line 1966 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 1994 | E501 | Line 1994 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 2007 | E501 | Line 2007 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 2024 | E501 | Line 2024 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 2050 | E501 | Line 2050 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 2078 | E501 | Line 2078 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 2106 | E501 | Line 2106 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 2134 | E501 | Line 2134 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 2160 | E501 | Line 2160 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 2186 | E501 | Line 2186 exceeds line length limit (Line too long (122 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 2214 | E501 | Line 2214 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 2240 | E501 | Line 2240 exceeds line length limit (Line too long (129 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.51.36/tests.py | 2268 | E501 | Line 2268 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 25 | E501 | Line 25 exceeds line length limit (Line too long (114 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 33 | E501 | Line 33 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 46 | E501 | Line 46 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 64 | E501 | Line 64 exceeds line length limit (Line too long (149 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 72 | E501 | Line 72 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 84 | E501 | Line 84 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 85 | E501 | Line 85 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 88 | E501 | Line 88 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 92 | E501 | Line 92 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 106 | E501 | Line 106 exceeds line length limit (Line too long (144 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 114 | E501 | Line 114 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 126 | E501 | Line 126 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 127 | E501 | Line 127 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 130 | E501 | Line 130 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 134 | E501 | Line 134 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 148 | E501 | Line 148 exceeds line length limit (Line too long (135 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 156 | E501 | Line 156 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 168 | E501 | Line 168 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 169 | E501 | Line 169 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 172 | E501 | Line 172 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 176 | E501 | Line 176 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 190 | E501 | Line 190 exceeds line length limit (Line too long (173 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 198 | E501 | Line 198 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 210 | E501 | Line 210 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 211 | E501 | Line 211 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 214 | E501 | Line 214 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 218 | E501 | Line 218 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 232 | E501 | Line 232 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 240 | E501 | Line 240 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 252 | E501 | Line 252 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 253 | E501 | Line 253 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 256 | E501 | Line 256 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 260 | E501 | Line 260 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 274 | E501 | Line 274 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 281 | E501 | Line 281 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 282 | E501 | Line 282 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 285 | E501 | Line 285 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 289 | E501 | Line 289 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 303 | E501 | Line 303 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 311 | E501 | Line 311 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 324 | E501 | Line 324 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 342 | E501 | Line 342 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 350 | E501 | Line 350 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 363 | E501 | Line 363 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 381 | E501 | Line 381 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 389 | E501 | Line 389 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 402 | E501 | Line 402 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 426 | E501 | Line 426 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 439 | E501 | Line 439 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 460 | E501 | Line 460 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 468 | E501 | Line 468 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 481 | E501 | Line 481 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 499 | E501 | Line 499 exceeds line length limit (Line too long (138 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 507 | E501 | Line 507 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 520 | E501 | Line 520 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 546 | E501 | Line 546 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 559 | E501 | Line 559 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 590 | E501 | Line 590 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 603 | E501 | Line 603 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 626 | E501 | Line 626 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 634 | E501 | Line 634 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 647 | E501 | Line 647 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 665 | E501 | Line 665 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 673 | E501 | Line 673 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 686 | E501 | Line 686 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 710 | E501 | Line 710 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 723 | E501 | Line 723 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 744 | E501 | Line 744 exceeds line length limit (Line too long (137 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 752 | E501 | Line 752 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 765 | E501 | Line 765 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 783 | E501 | Line 783 exceeds line length limit (Line too long (136 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 791 | E501 | Line 791 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 804 | E501 | Line 804 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 822 | E501 | Line 822 exceeds line length limit (Line too long (135 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 830 | E501 | Line 830 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 843 | E501 | Line 843 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 861 | E501 | Line 861 exceeds line length limit (Line too long (136 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 869 | E501 | Line 869 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 882 | E501 | Line 882 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 900 | E501 | Line 900 exceeds line length limit (Line too long (108 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 908 | E501 | Line 908 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 921 | E501 | Line 921 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 939 | E501 | Line 939 exceeds line length limit (Line too long (111 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 947 | E501 | Line 947 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 960 | E501 | Line 960 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 978 | E501 | Line 978 exceeds line length limit (Line too long (108 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 986 | E501 | Line 986 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 999 | E501 | Line 999 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1017 | E501 | Line 1017 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1025 | E501 | Line 1025 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1038 | E501 | Line 1038 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1062 | E501 | Line 1062 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1075 | E501 | Line 1075 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1096 | E501 | Line 1096 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1104 | E501 | Line 1104 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1117 | E501 | Line 1117 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1135 | E501 | Line 1135 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1143 | E501 | Line 1143 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1156 | E501 | Line 1156 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1174 | E501 | Line 1174 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1182 | E501 | Line 1182 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1195 | E501 | Line 1195 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1213 | E501 | Line 1213 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1221 | E501 | Line 1221 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1234 | E501 | Line 1234 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1252 | E501 | Line 1252 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1260 | E501 | Line 1260 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1273 | E501 | Line 1273 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1297 | E501 | Line 1297 exceeds line length limit (Line too long (105 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1315 | E501 | Line 1315 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1323 | E501 | Line 1323 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1336 | E501 | Line 1336 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1354 | E501 | Line 1354 exceeds line length limit (Line too long (136 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1362 | E501 | Line 1362 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1375 | E501 | Line 1375 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1400 | E501 | Line 1400 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1428 | E501 | Line 1428 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1454 | E501 | Line 1454 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1480 | E501 | Line 1480 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1493 | E501 | Line 1493 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1510 | E501 | Line 1510 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1527 | E501 | Line 1527 exceeds line length limit (Line too long (120 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1538 | E501 | Line 1538 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1541 | E501 | Line 1541 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1545 | E501 | Line 1545 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1567 | E501 | Line 1567 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1593 | E501 | Line 1593 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1619 | E501 | Line 1619 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1645 | E501 | Line 1645 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1674 | E501 | Line 1674 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1700 | E501 | Line 1700 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1728 | E501 | Line 1728 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1759 | E501 | Line 1759 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1785 | E501 | Line 1785 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1813 | E501 | Line 1813 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1839 | E501 | Line 1839 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1868 | E501 | Line 1868 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1894 | E501 | Line 1894 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1920 | E501 | Line 1920 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1948 | E501 | Line 1948 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 1974 | E501 | Line 1974 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 2000 | E501 | Line 2000 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 2026 | E501 | Line 2026 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 2052 | E501 | Line 2052 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 2078 | E501 | Line 2078 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 2107 | E501 | Line 2107 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 2133 | E501 | Line 2133 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 2159 | E501 | Line 2159 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 2185 | E501 | Line 2185 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 2213 | E501 | Line 2213 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 2239 | E501 | Line 2239 exceeds line length limit (Line too long (105 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 2265 | E501 | Line 2265 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.53.39/tests.py | 2291 | E501 | Line 2291 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 24 | E501 | Line 24 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 34 | E501 | Line 34 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 52 | E501 | Line 52 exceeds line length limit (Line too long (114 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 60 | E501 | Line 60 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 73 | E501 | Line 73 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 91 | E501 | Line 91 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 99 | E501 | Line 99 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 112 | E501 | Line 112 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 130 | E501 | Line 130 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 138 | E501 | Line 138 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 151 | E501 | Line 151 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 175 | E501 | Line 175 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 188 | E501 | Line 188 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 209 | E501 | Line 209 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 217 | E501 | Line 217 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 230 | E501 | Line 230 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 248 | E501 | Line 248 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 256 | E501 | Line 256 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 269 | E501 | Line 269 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 287 | E501 | Line 287 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 295 | E501 | Line 295 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 308 | E501 | Line 308 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 326 | E501 | Line 326 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 334 | E501 | Line 334 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 347 | E501 | Line 347 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 365 | E501 | Line 365 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 373 | E501 | Line 373 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 386 | E501 | Line 386 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 404 | E501 | Line 404 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 412 | E501 | Line 412 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 425 | E501 | Line 425 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 443 | E501 | Line 443 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 451 | E501 | Line 451 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 464 | E501 | Line 464 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 482 | E501 | Line 482 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 490 | E501 | Line 490 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 503 | E501 | Line 503 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 521 | E501 | Line 521 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 529 | E501 | Line 529 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 542 | E501 | Line 542 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 568 | E501 | Line 568 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 581 | E501 | Line 581 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 597 | E501 | Line 597 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 623 | E501 | Line 623 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 636 | E501 | Line 636 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 652 | E501 | Line 652 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 678 | E501 | Line 678 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 691 | E501 | Line 691 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 707 | E501 | Line 707 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 725 | E501 | Line 725 exceeds line length limit (Line too long (103 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 733 | E501 | Line 733 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 746 | E501 | Line 746 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 762 | E501 | Line 762 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 780 | E501 | Line 780 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 788 | E501 | Line 788 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 801 | E501 | Line 801 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 817 | E501 | Line 817 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 835 | E501 | Line 835 exceeds line length limit (Line too long (255 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 843 | E501 | Line 843 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 856 | E501 | Line 856 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 868 | E501 | Line 868 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 869 | E501 | Line 869 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 872 | E501 | Line 872 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 876 | E501 | Line 876 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 885 | E501 | Line 885 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 906 | E501 | Line 906 exceeds line length limit (Line too long (254 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 914 | E501 | Line 914 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 927 | E501 | Line 927 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 939 | E501 | Line 939 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 940 | E501 | Line 940 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 943 | E501 | Line 943 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 947 | E501 | Line 947 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 956 | E501 | Line 956 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 977 | E501 | Line 977 exceeds line length limit (Line too long (178 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 985 | E501 | Line 985 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 997 | E501 | Line 997 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 998 | E501 | Line 998 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1001 | E501 | Line 1001 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1005 | E501 | Line 1005 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1014 | E501 | Line 1014 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1035 | E501 | Line 1035 exceeds line length limit (Line too long (169 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1043 | E501 | Line 1043 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1055 | E501 | Line 1055 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1056 | E501 | Line 1056 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1059 | E501 | Line 1059 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1063 | E501 | Line 1063 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1072 | E501 | Line 1072 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1093 | E501 | Line 1093 exceeds line length limit (Line too long (185 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1101 | E501 | Line 1101 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1114 | E501 | Line 1114 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1129 | E501 | Line 1129 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1130 | E501 | Line 1130 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1133 | E501 | Line 1133 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1137 | E501 | Line 1137 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1146 | E501 | Line 1146 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1167 | E501 | Line 1167 exceeds line length limit (Line too long (187 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1175 | E501 | Line 1175 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1188 | E501 | Line 1188 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1203 | E501 | Line 1203 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1204 | E501 | Line 1204 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1207 | E501 | Line 1207 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1211 | E501 | Line 1211 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1220 | E501 | Line 1220 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1241 | E501 | Line 1241 exceeds line length limit (Line too long (258 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1249 | E501 | Line 1249 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1262 | E501 | Line 1262 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1274 | E501 | Line 1274 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1275 | E501 | Line 1275 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1278 | E501 | Line 1278 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1282 | E501 | Line 1282 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1291 | E501 | Line 1291 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1312 | E501 | Line 1312 exceeds line length limit (Line too long (185 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1320 | E501 | Line 1320 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1332 | E501 | Line 1332 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1333 | E501 | Line 1333 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1336 | E501 | Line 1336 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1340 | E501 | Line 1340 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1349 | E501 | Line 1349 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1370 | E501 | Line 1370 exceeds line length limit (Line too long (203 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1378 | E501 | Line 1378 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1391 | E501 | Line 1391 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1406 | E501 | Line 1406 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1407 | E501 | Line 1407 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1410 | E501 | Line 1410 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1414 | E501 | Line 1414 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1423 | E501 | Line 1423 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1444 | E501 | Line 1444 exceeds line length limit (Line too long (258 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1452 | E501 | Line 1452 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1465 | E501 | Line 1465 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1477 | E501 | Line 1477 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1478 | E501 | Line 1478 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1481 | E501 | Line 1481 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1485 | E501 | Line 1485 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1494 | E501 | Line 1494 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1523 | E501 | Line 1523 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1536 | E501 | Line 1536 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1552 | E501 | Line 1552 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1570 | E501 | Line 1570 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1578 | E501 | Line 1578 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1591 | E501 | Line 1591 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1607 | E501 | Line 1607 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1625 | E501 | Line 1625 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1633 | E501 | Line 1633 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1646 | E501 | Line 1646 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1662 | E501 | Line 1662 exceeds line length limit (Line too long (124 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1688 | E501 | Line 1688 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1701 | E501 | Line 1701 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1717 | E501 | Line 1717 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1743 | E501 | Line 1743 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1756 | E501 | Line 1756 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1772 | E501 | Line 1772 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1798 | E501 | Line 1798 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1811 | E501 | Line 1811 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1827 | E501 | Line 1827 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1845 | E501 | Line 1845 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1853 | E501 | Line 1853 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1866 | E501 | Line 1866 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1882 | E501 | Line 1882 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1908 | E501 | Line 1908 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1921 | E501 | Line 1921 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1937 | E501 | Line 1937 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1955 | E501 | Line 1955 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1963 | E501 | Line 1963 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1976 | E501 | Line 1976 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 1992 | E501 | Line 1992 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2018 | E501 | Line 2018 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2031 | E501 | Line 2031 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2057 | E501 | Line 2057 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2070 | E501 | Line 2070 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2096 | E501 | Line 2096 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2109 | E501 | Line 2109 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2135 | E501 | Line 2135 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2148 | E501 | Line 2148 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2173 | E501 | Line 2173 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2201 | E501 | Line 2201 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2227 | E501 | Line 2227 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2253 | E501 | Line 2253 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2266 | E501 | Line 2266 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2283 | E501 | Line 2283 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2300 | E501 | Line 2300 exceeds line length limit (Line too long (120 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2311 | E501 | Line 2311 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2314 | E501 | Line 2314 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2318 | E501 | Line 2318 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2340 | E501 | Line 2340 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2366 | E501 | Line 2366 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2392 | E501 | Line 2392 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2418 | E501 | Line 2418 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2447 | E501 | Line 2447 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2473 | E501 | Line 2473 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2502 | E501 | Line 2502 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2530 | E501 | Line 2530 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2556 | E501 | Line 2556 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2582 | E501 | Line 2582 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2608 | E501 | Line 2608 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2634 | E501 | Line 2634 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2660 | E501 | Line 2660 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2686 | E501 | Line 2686 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2712 | E501 | Line 2712 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2738 | E501 | Line 2738 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2764 | E501 | Line 2764 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2790 | E501 | Line 2790 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2816 | E501 | Line 2816 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2844 | E501 | Line 2844 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2873 | E501 | Line 2873 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2899 | E501 | Line 2899 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2927 | E501 | Line 2927 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2956 | E501 | Line 2956 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 2985 | E501 | Line 2985 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 3011 | E501 | Line 3011 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 3039 | E501 | Line 3039 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 3065 | E501 | Line 3065 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 3091 | E501 | Line 3091 exceeds line length limit (Line too long (124 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 3119 | E501 | Line 3119 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 3145 | E501 | Line 3145 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 3171 | E501 | Line 3171 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/21.57.50/tests.py | 3197 | E501 | Line 3197 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 24 | E501 | Line 24 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 34 | E501 | Line 34 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 52 | E501 | Line 52 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 60 | E501 | Line 60 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 73 | E501 | Line 73 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 91 | E501 | Line 91 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 99 | E501 | Line 99 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 112 | E501 | Line 112 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 136 | E501 | Line 136 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 149 | E501 | Line 149 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 170 | E501 | Line 170 exceeds line length limit (Line too long (222 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 178 | E501 | Line 178 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 191 | E501 | Line 191 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 203 | E501 | Line 203 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 204 | E501 | Line 204 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 207 | E501 | Line 207 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 211 | E501 | Line 211 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 225 | E501 | Line 225 exceeds line length limit (Line too long (221 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 233 | E501 | Line 233 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 246 | E501 | Line 246 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 258 | E501 | Line 258 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 259 | E501 | Line 259 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 262 | E501 | Line 262 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 266 | E501 | Line 266 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 280 | E501 | Line 280 exceeds line length limit (Line too long (149 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 288 | E501 | Line 288 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 300 | E501 | Line 300 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 301 | E501 | Line 301 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 304 | E501 | Line 304 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 308 | E501 | Line 308 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 322 | E501 | Line 322 exceeds line length limit (Line too long (144 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 330 | E501 | Line 330 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 342 | E501 | Line 342 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 343 | E501 | Line 343 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 346 | E501 | Line 346 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 350 | E501 | Line 350 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 364 | E501 | Line 364 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 372 | E501 | Line 372 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 385 | E501 | Line 385 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 400 | E501 | Line 400 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 401 | E501 | Line 401 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 404 | E501 | Line 404 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 408 | E501 | Line 408 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 422 | E501 | Line 422 exceeds line length limit (Line too long (224 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 430 | E501 | Line 430 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 443 | E501 | Line 443 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 455 | E501 | Line 455 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 456 | E501 | Line 456 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 459 | E501 | Line 459 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 463 | E501 | Line 463 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 477 | E501 | Line 477 exceeds line length limit (Line too long (224 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 485 | E501 | Line 485 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 498 | E501 | Line 498 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 510 | E501 | Line 510 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 511 | E501 | Line 511 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 514 | E501 | Line 514 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 518 | E501 | Line 518 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 532 | E501 | Line 532 exceeds line length limit (Line too long (224 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 540 | E501 | Line 540 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 553 | E501 | Line 553 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 565 | E501 | Line 565 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 566 | E501 | Line 566 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 569 | E501 | Line 569 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 573 | E501 | Line 573 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 587 | E501 | Line 587 exceeds line length limit (Line too long (220 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 595 | E501 | Line 595 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 608 | E501 | Line 608 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 620 | E501 | Line 620 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 621 | E501 | Line 621 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 624 | E501 | Line 624 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 628 | E501 | Line 628 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 642 | E501 | Line 642 exceeds line length limit (Line too long (289 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 650 | E501 | Line 650 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 663 | E501 | Line 663 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 681 | E501 | Line 681 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 694 | E501 | Line 694 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 706 | E501 | Line 706 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 707 | E501 | Line 707 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 710 | E501 | Line 710 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 714 | E501 | Line 714 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 728 | E501 | Line 728 exceeds line length limit (Line too long (288 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 736 | E501 | Line 736 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 749 | E501 | Line 749 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 767 | E501 | Line 767 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 780 | E501 | Line 780 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 792 | E501 | Line 792 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 793 | E501 | Line 793 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 796 | E501 | Line 796 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 800 | E501 | Line 800 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 814 | E501 | Line 814 exceeds line length limit (Line too long (216 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 822 | E501 | Line 822 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 835 | E501 | Line 835 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 853 | E501 | Line 853 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 865 | E501 | Line 865 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 866 | E501 | Line 866 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 869 | E501 | Line 869 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 873 | E501 | Line 873 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 893 | E501 | Line 893 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 906 | E501 | Line 906 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 935 | E501 | Line 935 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 948 | E501 | Line 948 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 969 | E501 | Line 969 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 977 | E501 | Line 977 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 990 | E501 | Line 990 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1008 | E501 | Line 1008 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1016 | E501 | Line 1016 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1029 | E501 | Line 1029 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1047 | E501 | Line 1047 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1055 | E501 | Line 1055 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1068 | E501 | Line 1068 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1086 | E501 | Line 1086 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1094 | E501 | Line 1094 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1107 | E501 | Line 1107 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1125 | E501 | Line 1125 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1133 | E501 | Line 1133 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1146 | E501 | Line 1146 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1164 | E501 | Line 1164 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1172 | E501 | Line 1172 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1185 | E501 | Line 1185 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1203 | E501 | Line 1203 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1211 | E501 | Line 1211 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1224 | E501 | Line 1224 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1242 | E501 | Line 1242 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1250 | E501 | Line 1250 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1263 | E501 | Line 1263 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1281 | E501 | Line 1281 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1299 | E501 | Line 1299 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1307 | E501 | Line 1307 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1320 | E501 | Line 1320 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1338 | E501 | Line 1338 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1364 | E501 | Line 1364 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1377 | E501 | Line 1377 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1393 | E501 | Line 1393 exceeds line length limit (Line too long (114 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1411 | E501 | Line 1411 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1419 | E501 | Line 1419 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1432 | E501 | Line 1432 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1448 | E501 | Line 1448 exceeds line length limit (Line too long (134 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1474 | E501 | Line 1474 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1487 | E501 | Line 1487 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1503 | E501 | Line 1503 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1521 | E501 | Line 1521 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1529 | E501 | Line 1529 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1542 | E501 | Line 1542 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1560 | E501 | Line 1560 exceeds line length limit (Line too long (179 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1568 | E501 | Line 1568 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1581 | E501 | Line 1581 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1599 | E501 | Line 1599 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1612 | E501 | Line 1612 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1630 | E501 | Line 1630 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1638 | E501 | Line 1638 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1651 | E501 | Line 1651 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1667 | E501 | Line 1667 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1693 | E501 | Line 1693 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1706 | E501 | Line 1706 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1722 | E501 | Line 1722 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1748 | E501 | Line 1748 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1761 | E501 | Line 1761 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1777 | E501 | Line 1777 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1803 | E501 | Line 1803 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1816 | E501 | Line 1816 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1842 | E501 | Line 1842 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1855 | E501 | Line 1855 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1881 | E501 | Line 1881 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1894 | E501 | Line 1894 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1925 | E501 | Line 1925 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1938 | E501 | Line 1938 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1964 | E501 | Line 1964 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 1977 | E501 | Line 1977 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2002 | E501 | Line 2002 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2030 | E501 | Line 2030 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2056 | E501 | Line 2056 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2082 | E501 | Line 2082 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2095 | E501 | Line 2095 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2112 | E501 | Line 2112 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2138 | E501 | Line 2138 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2164 | E501 | Line 2164 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2190 | E501 | Line 2190 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2216 | E501 | Line 2216 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2245 | E501 | Line 2245 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2262 | E501 | Line 2262 exceeds line length limit (Line too long (120 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2273 | E501 | Line 2273 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2276 | E501 | Line 2276 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2280 | E501 | Line 2280 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2302 | E501 | Line 2302 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2331 | E501 | Line 2331 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2359 | E501 | Line 2359 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2385 | E501 | Line 2385 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2414 | E501 | Line 2414 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2440 | E501 | Line 2440 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2466 | E501 | Line 2466 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2492 | E501 | Line 2492 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2518 | E501 | Line 2518 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2544 | E501 | Line 2544 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2570 | E501 | Line 2570 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2596 | E501 | Line 2596 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2624 | E501 | Line 2624 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2650 | E501 | Line 2650 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2676 | E501 | Line 2676 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2702 | E501 | Line 2702 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2728 | E501 | Line 2728 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2754 | E501 | Line 2754 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2785 | E501 | Line 2785 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2814 | E501 | Line 2814 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2840 | E501 | Line 2840 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2866 | E501 | Line 2866 exceeds line length limit (Line too long (114 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2892 | E501 | Line 2892 exceeds line length limit (Line too long (134 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2920 | E501 | Line 2920 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2946 | E501 | Line 2946 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2972 | E501 | Line 2972 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 2998 | E501 | Line 2998 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.02.30/tests.py | 3024 | E501 | Line 3024 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 34 | E501 | Line 34 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 50 | E501 | Line 50 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 60 | E501 | Line 60 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 78 | E501 | Line 78 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 86 | E501 | Line 86 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 99 | E501 | Line 99 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 117 | E501 | Line 117 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 125 | E501 | Line 125 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 138 | E501 | Line 138 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 162 | E501 | Line 162 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 175 | E501 | Line 175 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 196 | E501 | Line 196 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 204 | E501 | Line 204 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 217 | E501 | Line 217 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 241 | E501 | Line 241 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 254 | E501 | Line 254 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 275 | E501 | Line 275 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 283 | E501 | Line 283 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 296 | E501 | Line 296 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 314 | E501 | Line 314 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 322 | E501 | Line 322 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 335 | E501 | Line 335 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 353 | E501 | Line 353 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 361 | E501 | Line 361 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 374 | E501 | Line 374 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 392 | E501 | Line 392 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 400 | E501 | Line 400 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 413 | E501 | Line 413 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 431 | E501 | Line 431 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 439 | E501 | Line 439 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 452 | E501 | Line 452 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 478 | E501 | Line 478 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 491 | E501 | Line 491 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 507 | E501 | Line 507 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 517 | E501 | Line 517 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 525 | E501 | Line 525 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 538 | E501 | Line 538 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 554 | E501 | Line 554 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 564 | E501 | Line 564 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 572 | E501 | Line 572 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 585 | E501 | Line 585 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 603 | E501 | Line 603 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 611 | E501 | Line 611 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 624 | E501 | Line 624 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 642 | E501 | Line 642 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 650 | E501 | Line 650 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 663 | E501 | Line 663 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 681 | E501 | Line 681 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 689 | E501 | Line 689 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 702 | E501 | Line 702 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 720 | E501 | Line 720 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 728 | E501 | Line 728 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 741 | E501 | Line 741 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 759 | E501 | Line 759 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 767 | E501 | Line 767 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 780 | E501 | Line 780 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 798 | E501 | Line 798 exceeds line length limit (Line too long (146 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 806 | E501 | Line 806 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 819 | E501 | Line 819 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 832 | E501 | Line 832 exceeds line length limit (Line too long (108 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 844 | E501 | Line 844 exceeds line length limit (Line too long (110 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 852 | E501 | Line 852 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 865 | E501 | Line 865 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 883 | E501 | Line 883 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 899 | E501 | Line 899 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 901 | E501 | Line 901 exceeds line length limit (Line too long (140 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 909 | E501 | Line 909 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 922 | E501 | Line 922 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 940 | E501 | Line 940 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 958 | E501 | Line 958 exceeds line length limit (Line too long (108 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 966 | E501 | Line 966 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 979 | E501 | Line 979 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 997 | E501 | Line 997 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1015 | E501 | Line 1015 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1023 | E501 | Line 1023 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1036 | E501 | Line 1036 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1054 | E501 | Line 1054 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1072 | E501 | Line 1072 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1080 | E501 | Line 1080 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1093 | E501 | Line 1093 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1111 | E501 | Line 1111 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1129 | E501 | Line 1129 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1137 | E501 | Line 1137 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1150 | E501 | Line 1150 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1168 | E501 | Line 1168 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1186 | E501 | Line 1186 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1194 | E501 | Line 1194 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1207 | E501 | Line 1207 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1225 | E501 | Line 1225 exceeds line length limit (Line too long (134 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1243 | E501 | Line 1243 exceeds line length limit (Line too long (111 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1251 | E501 | Line 1251 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1264 | E501 | Line 1264 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1282 | E501 | Line 1282 exceeds line length limit (Line too long (124 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1308 | E501 | Line 1308 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1326 | E501 | Line 1326 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1352 | E501 | Line 1352 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1365 | E501 | Line 1365 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1391 | E501 | Line 1391 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1404 | E501 | Line 1404 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1430 | E501 | Line 1430 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1443 | E501 | Line 1443 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1469 | E501 | Line 1469 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1482 | E501 | Line 1482 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1507 | E501 | Line 1507 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1535 | E501 | Line 1535 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1561 | E501 | Line 1561 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1587 | E501 | Line 1587 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1600 | E501 | Line 1600 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1617 | E501 | Line 1617 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1643 | E501 | Line 1643 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1669 | E501 | Line 1669 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1695 | E501 | Line 1695 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1721 | E501 | Line 1721 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1750 | E501 | Line 1750 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1776 | E501 | Line 1776 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1805 | E501 | Line 1805 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1833 | E501 | Line 1833 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1859 | E501 | Line 1859 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1888 | E501 | Line 1888 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1916 | E501 | Line 1916 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1942 | E501 | Line 1942 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1968 | E501 | Line 1968 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 1994 | E501 | Line 1994 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2020 | E501 | Line 2020 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2046 | E501 | Line 2046 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2072 | E501 | Line 2072 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2098 | E501 | Line 2098 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2124 | E501 | Line 2124 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2150 | E501 | Line 2150 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2181 | E501 | Line 2181 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2207 | E501 | Line 2207 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2233 | E501 | Line 2233 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2259 | E501 | Line 2259 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2285 | E501 | Line 2285 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2315 | E501 | Line 2315 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2328 | E501 | Line 2328 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2345 | E501 | Line 2345 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2373 | E501 | Line 2373 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2399 | E501 | Line 2399 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2425 | E501 | Line 2425 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2451 | E501 | Line 2451 exceeds line length limit (Line too long (134 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.10.10/tests.py | 2479 | E501 | Line 2479 exceeds line length limit (Line too long (124 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 24 | E501 | Line 24 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 34 | E501 | Line 34 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 52 | E501 | Line 52 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 60 | E501 | Line 60 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 73 | E501 | Line 73 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 91 | E501 | Line 91 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 99 | E501 | Line 99 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 112 | E501 | Line 112 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 136 | E501 | Line 136 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 149 | E501 | Line 149 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 170 | E501 | Line 170 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 178 | E501 | Line 178 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 191 | E501 | Line 191 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 215 | E501 | Line 215 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 228 | E501 | Line 228 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 249 | E501 | Line 249 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 257 | E501 | Line 257 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 270 | E501 | Line 270 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 288 | E501 | Line 288 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 296 | E501 | Line 296 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 309 | E501 | Line 309 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 327 | E501 | Line 327 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 335 | E501 | Line 335 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 348 | E501 | Line 348 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 366 | E501 | Line 366 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 374 | E501 | Line 374 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 387 | E501 | Line 387 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 405 | E501 | Line 405 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 413 | E501 | Line 413 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 426 | E501 | Line 426 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 452 | E501 | Line 452 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 465 | E501 | Line 465 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 481 | E501 | Line 481 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 491 | E501 | Line 491 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 499 | E501 | Line 499 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 512 | E501 | Line 512 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 528 | E501 | Line 528 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 538 | E501 | Line 538 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 546 | E501 | Line 546 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 559 | E501 | Line 559 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 577 | E501 | Line 577 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 585 | E501 | Line 585 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 598 | E501 | Line 598 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 616 | E501 | Line 616 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 624 | E501 | Line 624 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 637 | E501 | Line 637 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 655 | E501 | Line 655 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 663 | E501 | Line 663 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 676 | E501 | Line 676 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 694 | E501 | Line 694 exceeds line length limit (Line too long (146 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 702 | E501 | Line 702 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 715 | E501 | Line 715 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 728 | E501 | Line 728 exceeds line length limit (Line too long (108 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 740 | E501 | Line 740 exceeds line length limit (Line too long (110 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 748 | E501 | Line 748 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 761 | E501 | Line 761 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 779 | E501 | Line 779 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 795 | E501 | Line 795 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 797 | E501 | Line 797 exceeds line length limit (Line too long (140 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 805 | E501 | Line 805 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 818 | E501 | Line 818 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 836 | E501 | Line 836 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 854 | E501 | Line 854 exceeds line length limit (Line too long (108 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 862 | E501 | Line 862 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 875 | E501 | Line 875 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 893 | E501 | Line 893 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 911 | E501 | Line 911 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 919 | E501 | Line 919 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 932 | E501 | Line 932 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 950 | E501 | Line 950 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 968 | E501 | Line 968 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 976 | E501 | Line 976 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 989 | E501 | Line 989 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1007 | E501 | Line 1007 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1025 | E501 | Line 1025 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1033 | E501 | Line 1033 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1046 | E501 | Line 1046 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1064 | E501 | Line 1064 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1082 | E501 | Line 1082 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1090 | E501 | Line 1090 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1103 | E501 | Line 1103 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1121 | E501 | Line 1121 exceeds line length limit (Line too long (134 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1139 | E501 | Line 1139 exceeds line length limit (Line too long (111 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1147 | E501 | Line 1147 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1160 | E501 | Line 1160 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1178 | E501 | Line 1178 exceeds line length limit (Line too long (124 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1204 | E501 | Line 1204 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1222 | E501 | Line 1222 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1248 | E501 | Line 1248 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1261 | E501 | Line 1261 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1287 | E501 | Line 1287 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1300 | E501 | Line 1300 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1326 | E501 | Line 1326 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1339 | E501 | Line 1339 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1365 | E501 | Line 1365 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1378 | E501 | Line 1378 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1403 | E501 | Line 1403 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1431 | E501 | Line 1431 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1457 | E501 | Line 1457 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1483 | E501 | Line 1483 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1496 | E501 | Line 1496 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1513 | E501 | Line 1513 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1539 | E501 | Line 1539 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1565 | E501 | Line 1565 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1591 | E501 | Line 1591 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1617 | E501 | Line 1617 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1646 | E501 | Line 1646 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1672 | E501 | Line 1672 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1701 | E501 | Line 1701 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1729 | E501 | Line 1729 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1755 | E501 | Line 1755 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1784 | E501 | Line 1784 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1812 | E501 | Line 1812 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1838 | E501 | Line 1838 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1864 | E501 | Line 1864 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1890 | E501 | Line 1890 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1916 | E501 | Line 1916 exceeds line length limit (Line too long (150 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1942 | E501 | Line 1942 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1968 | E501 | Line 1968 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 1994 | E501 | Line 1994 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 2020 | E501 | Line 2020 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 2046 | E501 | Line 2046 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 2077 | E501 | Line 2077 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 2103 | E501 | Line 2103 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 2129 | E501 | Line 2129 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 2155 | E501 | Line 2155 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 2181 | E501 | Line 2181 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 2211 | E501 | Line 2211 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 2224 | E501 | Line 2224 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 2241 | E501 | Line 2241 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 2269 | E501 | Line 2269 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 2295 | E501 | Line 2295 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 2321 | E501 | Line 2321 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 2347 | E501 | Line 2347 exceeds line length limit (Line too long (134 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 2375 | E501 | Line 2375 exceeds line length limit (Line too long (124 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/06-02-2026/22.17.56/tests.py | 2395 | E501 | Line 2395 exceeds line length limit (Line too long (131 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 22 | E501 | Line 22 exceeds line length limit (Line too long (162 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 23 | E501 | Line 23 exceeds line length limit (Line too long (159 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 25 | E501 | Line 25 exceeds line length limit (Line too long (161 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 28 | E501 | Line 28 exceeds line length limit (Line too long (170 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 29 | E501 | Line 29 exceeds line length limit (Line too long (94 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 34 | E501 | Line 34 exceeds line length limit (Line too long (134 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 35 | E501 | Line 35 exceeds line length limit (Line too long (132 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 36 | E501 | Line 36 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 37 | E501 | Line 37 exceeds line length limit (Line too long (164 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 38 | E501 | Line 38 exceeds line length limit (Line too long (141 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 39 | E501 | Line 39 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 40 | E501 | Line 40 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 41 | E501 | Line 41 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 42 | E501 | Line 42 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 43 | E501 | Line 43 exceeds line length limit (Line too long (148 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 44 | E501 | Line 44 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 45 | E501 | Line 45 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 46 | E501 | Line 46 exceeds line length limit (Line too long (158 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 47 | E501 | Line 47 exceeds line length limit (Line too long (142 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 48 | E501 | Line 48 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 49 | E501 | Line 49 exceeds line length limit (Line too long (149 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 50 | E501 | Line 50 exceeds line length limit (Line too long (126 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 51 | E501 | Line 51 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 52 | E501 | Line 52 exceeds line length limit (Line too long (158 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 53 | E501 | Line 53 exceeds line length limit (Line too long (135 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 54 | E501 | Line 54 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 55 | E501 | Line 55 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 56 | E501 | Line 56 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 57 | E501 | Line 57 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 58 | E501 | Line 58 exceeds line length limit (Line too long (158 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 59 | E501 | Line 59 exceeds line length limit (Line too long (138 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 60 | E501 | Line 60 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 61 | E501 | Line 61 exceeds line length limit (Line too long (158 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 62 | E501 | Line 62 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 63 | E501 | Line 63 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 64 | E501 | Line 64 exceeds line length limit (Line too long (149 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 65 | E501 | Line 65 exceeds line length limit (Line too long (126 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 66 | E501 | Line 66 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 67 | E501 | Line 67 exceeds line length limit (Line too long (159 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 68 | E501 | Line 68 exceeds line length limit (Line too long (136 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 69 | E501 | Line 69 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 70 | E501 | Line 70 exceeds line length limit (Line too long (158 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 71 | E501 | Line 71 exceeds line length limit (Line too long (143 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 72 | E501 | Line 72 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 73 | E501 | Line 73 exceeds line length limit (Line too long (159 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 74 | E501 | Line 74 exceeds line length limit (Line too long (136 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 75 | E501 | Line 75 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 76 | E501 | Line 76 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 77 | E501 | Line 77 exceeds line length limit (Line too long (122 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 79 | E501 | Line 79 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 80 | E501 | Line 80 exceeds line length limit (Line too long (124 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 81 | E501 | Line 81 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 82 | E501 | Line 82 exceeds line length limit (Line too long (124 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/scenario_tests.py | 78 | E501 | Line 78 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/scenario_tests.py | 88 | E501 | Line 88 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/scenario_tests.py | 98 | E501 | Line 98 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/scenario_tests.py | 108 | E501 | Line 108 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/scenario_tests.py | 118 | E501 | Line 118 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 22 | E501 | Line 22 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 31 | E501 | Line 31 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 33 | E501 | Line 33 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 38 | E501 | Line 38 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 39 | E501 | Line 39 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 47 | E501 | Line 47 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 49 | E501 | Line 49 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 54 | E501 | Line 54 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 57 | E501 | Line 57 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 63 | E501 | Line 63 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 65 | E501 | Line 65 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 70 | E501 | Line 70 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 72 | E501 | Line 72 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 77 | E501 | Line 77 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 80 | E501 | Line 80 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 86 | E501 | Line 86 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 88 | E501 | Line 88 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 93 | E501 | Line 93 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 95 | E501 | Line 95 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 100 | E501 | Line 100 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 103 | E501 | Line 103 exceeds line length limit (Line too long (114 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 109 | E501 | Line 109 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 111 | E501 | Line 111 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 116 | E501 | Line 116 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 118 | E501 | Line 118 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 132 | E501 | Line 132 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 134 | E501 | Line 134 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 139 | E501 | Line 139 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 141 | E501 | Line 141 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 146 | E501 | Line 146 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 149 | E501 | Line 149 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 155 | E501 | Line 155 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 157 | E501 | Line 157 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 162 | E501 | Line 162 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 164 | E501 | Line 164 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 179 | E501 | Line 179 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 181 | E501 | Line 181 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 184 | E501 | Line 184 exceeds line length limit (Line too long (94 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 197 | E501 | Line 197 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 199 | E501 | Line 199 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 215 | E501 | Line 215 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 217 | E501 | Line 217 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 233 | E501 | Line 233 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 235 | E501 | Line 235 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 238 | E501 | Line 238 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 251 | E501 | Line 251 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 253 | E501 | Line 253 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 269 | E501 | Line 269 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 271 | E501 | Line 271 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 287 | E501 | Line 287 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 289 | E501 | Line 289 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 305 | E501 | Line 305 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 307 | E501 | Line 307 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 323 | E501 | Line 323 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 325 | E501 | Line 325 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 332 | E501 | Line 332 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 333 | E501 | Line 333 exceeds line length limit (Line too long (131 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/landing_page.py | 22 | E501 | Line 22 exceeds line length limit (Line too long (162 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/landing_page.py | 23 | E501 | Line 23 exceeds line length limit (Line too long (159 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/landing_page.py | 25 | E501 | Line 25 exceeds line length limit (Line too long (161 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/landing_page.py | 28 | E501 | Line 28 exceeds line length limit (Line too long (170 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/landing_page.py | 29 | E501 | Line 29 exceeds line length limit (Line too long (94 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 22 | E501 | Line 22 exceeds line length limit (Line too long (162 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 23 | E501 | Line 23 exceeds line length limit (Line too long (159 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 25 | E501 | Line 25 exceeds line length limit (Line too long (161 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 28 | E501 | Line 28 exceeds line length limit (Line too long (170 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 29 | E501 | Line 29 exceeds line length limit (Line too long (94 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 33 | E501 | Line 33 exceeds line length limit (Line too long (148 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 34 | E501 | Line 34 exceeds line length limit (Line too long (131 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 35 | E501 | Line 35 exceeds line length limit (Line too long (131 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 36 | E501 | Line 36 exceeds line length limit (Line too long (120 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 37 | E501 | Line 37 exceeds line length limit (Line too long (111 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 38 | E501 | Line 38 exceeds line length limit (Line too long (131 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 39 | E501 | Line 39 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 40 | E501 | Line 40 exceeds line length limit (Line too long (122 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 41 | E501 | Line 41 exceeds line length limit (Line too long (118 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 42 | E501 | Line 42 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 43 | E501 | Line 43 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 44 | E501 | Line 44 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 45 | E501 | Line 45 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 46 | E501 | Line 46 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 47 | E501 | Line 47 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 48 | E501 | Line 48 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 49 | E501 | Line 49 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 50 | E501 | Line 50 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 51 | E501 | Line 51 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 52 | E501 | Line 52 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 53 | E501 | Line 53 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 54 | E501 | Line 54 exceeds line length limit (Line too long (118 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 55 | E501 | Line 55 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 56 | E501 | Line 56 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 57 | E501 | Line 57 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 58 | E501 | Line 58 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 59 | E501 | Line 59 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 60 | E501 | Line 60 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 61 | E501 | Line 61 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 62 | E501 | Line 62 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 63 | E501 | Line 63 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 64 | E501 | Line 64 exceeds line length limit (Line too long (118 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 65 | E501 | Line 65 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 66 | E501 | Line 66 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 67 | E501 | Line 67 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 68 | E501 | Line 68 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 69 | E501 | Line 69 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 70 | E501 | Line 70 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 71 | E501 | Line 71 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 72 | E501 | Line 72 exceeds line length limit (Line too long (115 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 73 | E501 | Line 73 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 74 | E501 | Line 74 exceeds line length limit (Line too long (114 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 75 | E501 | Line 75 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 76 | E501 | Line 76 exceeds line length limit (Line too long (114 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 77 | E501 | Line 77 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 79 | E501 | Line 79 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 80 | E501 | Line 80 exceeds line length limit (Line too long (92 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 81 | E501 | Line 81 exceeds line length limit (Line too long (103 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 82 | E501 | Line 82 exceeds line length limit (Line too long (127 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 83 | E501 | Line 83 exceeds line length limit (Line too long (118 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 84 | E501 | Line 84 exceeds line length limit (Line too long (124 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 85 | E501 | Line 85 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 86 | E501 | Line 86 exceeds line length limit (Line too long (160 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 87 | E501 | Line 87 exceeds line length limit (Line too long (147 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 88 | E501 | Line 88 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 89 | E501 | Line 89 exceeds line length limit (Line too long (158 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 90 | E501 | Line 90 exceeds line length limit (Line too long (135 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 91 | E501 | Line 91 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 92 | E501 | Line 92 exceeds line length limit (Line too long (160 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 93 | E501 | Line 93 exceeds line length limit (Line too long (137 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 94 | E501 | Line 94 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 95 | E501 | Line 95 exceeds line length limit (Line too long (149 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 96 | E501 | Line 96 exceeds line length limit (Line too long (126 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 97 | E501 | Line 97 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 98 | E501 | Line 98 exceeds line length limit (Line too long (162 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 99 | E501 | Line 99 exceeds line length limit (Line too long (139 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 100 | E501 | Line 100 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 101 | E501 | Line 101 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 102 | E501 | Line 102 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 103 | E501 | Line 103 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 104 | E501 | Line 104 exceeds line length limit (Line too long (162 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 105 | E501 | Line 105 exceeds line length limit (Line too long (139 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 106 | E501 | Line 106 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 107 | E501 | Line 107 exceeds line length limit (Line too long (158 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 108 | E501 | Line 108 exceeds line length limit (Line too long (143 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 109 | E501 | Line 109 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 110 | E501 | Line 110 exceeds line length limit (Line too long (148 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 111 | E501 | Line 111 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 112 | E501 | Line 112 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 113 | E501 | Line 113 exceeds line length limit (Line too long (164 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 114 | E501 | Line 114 exceeds line length limit (Line too long (141 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 115 | E501 | Line 115 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 116 | E501 | Line 116 exceeds line length limit (Line too long (158 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 117 | E501 | Line 117 exceeds line length limit (Line too long (138 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 118 | E501 | Line 118 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 119 | E501 | Line 119 exceeds line length limit (Line too long (162 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 120 | E501 | Line 120 exceeds line length limit (Line too long (139 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 121 | E501 | Line 121 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 122 | E501 | Line 122 exceeds line length limit (Line too long (162 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 123 | E501 | Line 123 exceeds line length limit (Line too long (139 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 124 | E501 | Line 124 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 125 | E501 | Line 125 exceeds line length limit (Line too long (158 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 126 | E501 | Line 126 exceeds line length limit (Line too long (142 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 127 | E501 | Line 127 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 128 | E501 | Line 128 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 129 | E501 | Line 129 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 131 | E501 | Line 131 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 132 | E501 | Line 132 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 133 | E501 | Line 133 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 134 | E501 | Line 134 exceeds line length limit (Line too long (112 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/tests.py | 22 | E501 | Line 22 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/tests.py | 25 | E501 | Line 25 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/tests.py | 30 | E501 | Line 30 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/tests.py | 31 | E501 | Line 31 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/tests.py | 32 | E501 | Line 32 exceeds line length limit (Line too long (193 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/tests.py | 34 | E501 | Line 34 exceeds line length limit (Line too long (108 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/tests.py | 35 | E501 | Line 35 exceeds line length limit (Line too long (142 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/tests.py | 36 | E501 | Line 36 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 22 | E501 | Line 22 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 31 | E501 | Line 31 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 32 | E501 | Line 32 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 35 | E501 | Line 35 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 49 | E501 | Line 49 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 50 | E501 | Line 50 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 53 | E501 | Line 53 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 58 | E501 | Line 58 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 61 | E501 | Line 61 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 67 | E501 | Line 67 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 68 | E501 | Line 68 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 71 | E501 | Line 71 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 76 | E501 | Line 76 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 77 | E501 | Line 77 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 80 | E501 | Line 80 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 85 | E501 | Line 85 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 88 | E501 | Line 88 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 94 | E501 | Line 94 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 95 | E501 | Line 95 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 98 | E501 | Line 98 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 103 | E501 | Line 103 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 104 | E501 | Line 104 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 107 | E501 | Line 107 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 121 | E501 | Line 121 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 122 | E501 | Line 122 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 125 | E501 | Line 125 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 130 | E501 | Line 130 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 131 | E501 | Line 131 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 134 | E501 | Line 134 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 139 | E501 | Line 139 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 142 | E501 | Line 142 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 148 | E501 | Line 148 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 149 | E501 | Line 149 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 152 | E501 | Line 152 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 157 | E501 | Line 157 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 158 | E501 | Line 158 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 161 | E501 | Line 161 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 166 | E501 | Line 166 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 169 | E501 | Line 169 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 175 | E501 | Line 175 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 176 | E501 | Line 176 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 179 | E501 | Line 179 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 184 | E501 | Line 184 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 185 | E501 | Line 185 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 188 | E501 | Line 188 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 193 | E501 | Line 193 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 196 | E501 | Line 196 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 202 | E501 | Line 202 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 203 | E501 | Line 203 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 206 | E501 | Line 206 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 211 | E501 | Line 211 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 212 | E501 | Line 212 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 215 | E501 | Line 215 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 220 | E501 | Line 220 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 223 | E501 | Line 223 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 229 | E501 | Line 229 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 230 | E501 | Line 230 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 233 | E501 | Line 233 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 238 | E501 | Line 238 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 239 | E501 | Line 239 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 242 | E501 | Line 242 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 247 | E501 | Line 247 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 250 | E501 | Line 250 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 256 | E501 | Line 256 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 257 | E501 | Line 257 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 260 | E501 | Line 260 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 265 | E501 | Line 265 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 266 | E501 | Line 266 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 269 | E501 | Line 269 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 274 | E501 | Line 274 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 283 | E501 | Line 283 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 284 | E501 | Line 284 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 287 | E501 | Line 287 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 292 | E501 | Line 292 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 301 | E501 | Line 301 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 302 | E501 | Line 302 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 305 | E501 | Line 305 exceeds line length limit (Line too long (105 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 310 | E501 | Line 310 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 313 | E501 | Line 313 exceeds line length limit (Line too long (151 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 319 | E501 | Line 319 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 320 | E501 | Line 320 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 323 | E501 | Line 323 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 327 | E501 | Line 327 exceeds line length limit (Line too long (119 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 328 | E501 | Line 328 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 329 | E501 | Line 329 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 331 | E501 | Line 331 exceeds line length limit (Line too long (142 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 332 | E501 | Line 332 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 337 | E501 | Line 337 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 340 | E501 | Line 340 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 346 | E501 | Line 346 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 347 | E501 | Line 347 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 350 | E501 | Line 350 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 355 | E501 | Line 355 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 364 | E501 | Line 364 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 365 | E501 | Line 365 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 368 | E501 | Line 368 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 373 | E501 | Line 373 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 376 | E501 | Line 376 exceeds line length limit (Line too long (131 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 382 | E501 | Line 382 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 383 | E501 | Line 383 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 386 | E501 | Line 386 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 391 | E501 | Line 391 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 400 | E501 | Line 400 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 401 | E501 | Line 401 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 404 | E501 | Line 404 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 409 | E501 | Line 409 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 412 | E501 | Line 412 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 418 | E501 | Line 418 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 419 | E501 | Line 419 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 422 | E501 | Line 422 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 427 | E501 | Line 427 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 436 | E501 | Line 436 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 437 | E501 | Line 437 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 440 | E501 | Line 440 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 445 | E501 | Line 445 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 454 | E501 | Line 454 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 455 | E501 | Line 455 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 458 | E501 | Line 458 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 463 | E501 | Line 463 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 472 | E501 | Line 472 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 473 | E501 | Line 473 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 476 | E501 | Line 476 exceeds line length limit (Line too long (108 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 491 | E501 | Line 491 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 492 | E501 | Line 492 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 495 | E501 | Line 495 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 498 | E501 | Line 498 exceeds line length limit (Line too long (94 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 511 | E501 | Line 511 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 512 | E501 | Line 512 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 515 | E501 | Line 515 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 531 | E501 | Line 531 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 532 | E501 | Line 532 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 535 | E501 | Line 535 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 550 | E501 | Line 550 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 551 | E501 | Line 551 exceeds line length limit (Line too long (145 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 554 | E501 | Line 554 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 569 | E501 | Line 569 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 570 | E501 | Line 570 exceeds line length limit (Line too long (123 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 573 | E501 | Line 573 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 576 | E501 | Line 576 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 589 | E501 | Line 589 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 590 | E501 | Line 590 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 593 | E501 | Line 593 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 609 | E501 | Line 609 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 610 | E501 | Line 610 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 613 | E501 | Line 613 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 628 | E501 | Line 628 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 629 | E501 | Line 629 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 632 | E501 | Line 632 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 647 | E501 | Line 647 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 648 | E501 | Line 648 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 651 | E501 | Line 651 exceeds line length limit (Line too long (116 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 666 | E501 | Line 666 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 667 | E501 | Line 667 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 670 | E501 | Line 670 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 686 | E501 | Line 686 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 687 | E501 | Line 687 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 690 | E501 | Line 690 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 706 | E501 | Line 706 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 707 | E501 | Line 707 exceeds line length limit (Line too long (154 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 710 | E501 | Line 710 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 725 | E501 | Line 725 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 726 | E501 | Line 726 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 729 | E501 | Line 729 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 745 | E501 | Line 745 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 746 | E501 | Line 746 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 749 | E501 | Line 749 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 765 | E501 | Line 765 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 766 | E501 | Line 766 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 769 | E501 | Line 769 exceeds line length limit (Line too long (105 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 775 | E501 | Line 775 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 776 | E501 | Line 776 exceeds line length limit (Line too long (120 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 785 | E501 | Line 785 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 786 | E501 | Line 786 exceeds line length limit (Line too long (194 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 788 | E501 | Line 788 exceeds line length limit (Line too long (142 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 789 | E501 | Line 789 exceeds line length limit (Line too long (130 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 805 | E501 | Line 805 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 806 | E501 | Line 806 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 809 | E501 | Line 809 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 825 | E501 | Line 825 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 826 | E501 | Line 826 exceeds line length limit (Line too long (153 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 829 | E501 | Line 829 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 845 | E501 | Line 845 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 846 | E501 | Line 846 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 849 | E501 | Line 849 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 865 | E501 | Line 865 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 866 | E501 | Line 866 exceeds line length limit (Line too long (97 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 869 | E501 | Line 869 exceeds line length limit (Line too long (108 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/scenario_tests.py | 78 | E501 | Line 78 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/scenario_tests.py | 89 | E501 | Line 89 exceeds line length limit (Line too long (91 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/scenario_tests.py | 100 | E501 | Line 100 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/scenario_tests.py | 122 | E501 | Line 122 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/analysis/archetype.py | 1 | E501 | Line 1 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/analysis/archetype.py | 136 | E501 | Line 136 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/analysis/archetype.py | 209 | E501 | Line 209 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/analysis/archetype.py | 211 | E501 | Line 211 exceeds line length limit (Line too long (91 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/analysis/archetype.py | 213 | E501 | Line 213 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/analysis/archetype.py | 215 | E501 | Line 215 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/analysis/site_model.py | 1 | E501 | Line 1 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/analysis/verdict.py | 80 | E501 | Line 80 exceeds line length limit (Line too long (94 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/analysis/verdict.py | 236 | E501 | Line 236 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/cli.py | 98 | E501 | Line 98 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/cli.py | 310 | E501 | Line 310 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/cli.py | 401 | E501 | Line 401 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/cli.py | 737 | E501 | Line 737 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/playwright_tests.py | 156 | E501 | Line 156 exceeds line length limit (Line too long (159 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/playwright_tests.py | 182 | E501 | Line 182 exceeds line length limit (Line too long (107 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/playwright_tests.py | 194 | E501 | Line 194 exceeds line length limit (Line too long (109 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/playwright_tests.py | 232 | E501 | Line 232 exceeds line length limit (Line too long (113 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/playwright_tests.py | 255 | E501 | Line 255 exceeds line length limit (Line too long (94 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/playwright_tests.py | 259 | E501 | Line 259 exceeds line length limit (Line too long (101 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/playwright_tests.py | 285 | E501 | Line 285 exceeds line length limit (Line too long (92 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/playwright_tests.py | 397 | E501 | Line 397 exceeds line length limit (Line too long (164 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/playwright_tests.py | 448 | E501 | Line 448 exceeds line length limit (Line too long (105 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/playwright_tests.py | 457 | E501 | Line 457 exceeds line length limit (Line too long (121 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/playwright_tests.py | 486 | E501 | Line 486 exceeds line length limit (Line too long (125 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/scenario_tests.py | 158 | E501 | Line 158 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/scenario_tests.py | 310 | E501 | Line 310 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/scenario_tests.py | 444 | E501 | Line 444 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/scenario_tests.py | 467 | E501 | Line 467 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/scenario_tests.py | 555 | E501 | Line 555 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/scenario_tests.py | 627 | E501 | Line 627 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/scenario_tests.py | 645 | E501 | Line 645 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/scenario_tests.py | 712 | E501 | Line 712 exceeds line length limit (Line too long (106 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/core/browser.py | 261 | E501 | Line 261 exceeds line length limit (Line too long (92 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/core/browser.py | 323 | E501 | Line 323 exceeds line length limit (Line too long (104 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/core/browser.py | 400 | E501 | Line 400 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/core/navigator.py | 192 | E501 | Line 192 exceeds line length limit (Line too long (91 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/core/navigator.py | 363 | E501 | Line 363 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/core/navigator.py | 405 | E501 | Line 405 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/core/navigator.py | 443 | E501 | Line 443 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/core/state.py | 173 | E501 | Line 173 exceeds line length limit (Line too long (94 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/discovery/actions.py | 376 | E501 | Line 376 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/discovery/elements.py | 1 | E501 | Line 1 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/discovery/elements.py | 405 | E501 | Line 405 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/reporting/terminal.py | 82 | E501 | Line 82 exceeds line length limit (Line too long (94 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/reporting/terminal.py | 132 | E501 | Line 132 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/reporting/terminal.py | 155 | E501 | Line 155 exceeds line length limit (Line too long (98 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/smart/planner.py | 189 | E501 | Line 189 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/smart/scenarios.py | 142 | E501 | Line 142 exceeds line length limit (Line too long (96 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/smart/scenarios.py | 149 | E501 | Line 149 exceeds line length limit (Line too long (94 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/storage/db.py | 123 | E501 | Line 123 exceeds line length limit (Line too long (90 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/storage/db.py | 411 | E501 | Line 411 exceeds line length limit (Line too long (91 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/storage/db.py | 412 | E501 | Line 412 exceeds line length limit (Line too long (91 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/storage/db.py | 413 | E501 | Line 413 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/storage/db.py | 414 | E501 | Line 414 exceeds line length limit (Line too long (152 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/storage/db.py | 422 | E501 | Line 422 exceeds line length limit (Line too long (99 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/storage/db.py | 444 | E501 | Line 444 exceeds line length limit (Line too long (93 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/storage/db.py | 482 | E501 | Line 482 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 226 | E501 | Line 226 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 25 | E501 | Line 25 exceeds line length limit (Line too long (103 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 33 | E501 | Line 33 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 14 | E501 | Line 14 exceeds line length limit (Line too long (95 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 228 | E501 | Line 228 exceeds line length limit (Line too long (92 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 242 | E501 | Line 242 exceeds line length limit (Line too long (92 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 301 | E501 | Line 301 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 96 | E501 | Line 96 exceeds line length limit (Line too long (91 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 97 | E501 | Line 97 exceeds line length limit (Line too long (91 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 236 | E501 | Line 236 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 237 | E501 | Line 237 exceeds line length limit (Line too long (102 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 239 | E501 | Line 239 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 240 | E501 | Line 240 exceeds line length limit (Line too long (117 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 256 | E501 | Line 256 exceeds line length limit (Line too long (94 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 263 | E501 | Line 263 exceeds line length limit (Line too long (105 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 265 | E501 | Line 265 exceeds line length limit (Line too long (100 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 324 | E501 | Line 324 exceeds line length limit (Line too long (89 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 373 | E501 | Line 373 exceeds line length limit (Line too long (105 > 88)) |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 375 | E501 | Line 375 exceeds line length limit (Line too long (103 > 88)) |

### sqlfluff (0 issues)
No issues found.

### markdownlint (1 issues)
No issues found.

### clippy (0 issues)
No issues found.

### oxfmt (2 issues)
| File | Line | Code | Message |
|------|------|------|---------|
| src/flowscout/js/page_analysis.ts | 1 | FORMAT | File is not formatted |
| src/flowscout/reporting/vendor/vis-network.min.js | 1 | FORMAT | File is not formatted |

### prettier (40 issues)
| File | Line | Code | Message |
|------|------|------|---------|
| .lintro/run-20260206-232113/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260206-232113/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260206-232224/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260206-232224/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-100845/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-100845/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-101348/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-101348/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-101813/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-101813/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-101854/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-101854/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-102055/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-102055/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-103114/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-103114/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-103511/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-103511/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-103557/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-103557/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-103739/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-103739/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-103801/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-103801/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-104030/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-104030/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-104228/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-104228/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-104518/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-104518/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-104720/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-104720/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-104857/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-104857/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-105104/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-105104/report.md | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-105405/report.html | 1 | FORMAT | Code style issues found |
| .lintro/run-20260209-105405/report.md | 1 | FORMAT | Code style issues found |
| README.md | 1 | FORMAT | Code style issues found |
| docs/V1_BASELINE_BENCHMARKS.md | 1 | FORMAT | Code style issues found |

### actionlint (0 issues)
No issues found.

### semgrep (6 issues)
| File | Line | Code | Message |
|------|------|------|---------|
| src/flowscout/reporting/html.py | 16 |  | [python.flask.security.xss.audit.direct-use-of-jinja2.direct-use-of-jinja2] WARNING: Detected direct use of jinja2. If not done properly, this may bypass HTML escaping which opens up the application to cross-site scripting (XSS) vulnerabilities. Prefer using the Flask method 'render_template()' and templates with a '.html' extension in order to prevent XSS. |
| src/flowscout/reporting/html.py | 106 |  | [python.flask.security.xss.audit.direct-use-of-jinja2.direct-use-of-jinja2] WARNING: Detected direct use of jinja2. If not done properly, this may bypass HTML escaping which opens up the application to cross-site scripting (XSS) vulnerabilities. Prefer using the Flask method 'render_template()' and templates with a '.html' extension in order to prevent XSS. |
| src/flowscout/reporting/html.py | 124 |  | [python.flask.security.xss.audit.explicit-unescape-with-markup.explicit-unescape-with-markup] WARNING: Detected explicitly unescaped content using 'Markup()'. This permits the unescaped data to include unescaped HTML which could result in cross-site scripting. Ensure this data is not externally controlled, or consider rewriting to not use 'Markup()'. |
| src/flowscout/reporting/html.py | 125 |  | [python.flask.security.xss.audit.explicit-unescape-with-markup.explicit-unescape-with-markup] WARNING: Detected explicitly unescaped content using 'Markup()'. This permits the unescaped data to include unescaped HTML which could result in cross-site scripting. Ensure this data is not externally controlled, or consider rewriting to not use 'Markup()'. |
| src/flowscout/storage/db.py | 183 |  | [python.lang.security.audit.formatted-sql-query.formatted-sql-query] WARNING: Detected possible formatted SQL query. Use parameterized queries instead. |
| src/flowscout/storage/db.py | 183 |  | [python.sqlalchemy.security.sqlalchemy-execute-raw-query.sqlalchemy-execute-raw-query] ERROR: Avoiding SQL string concatenation: untrusted input concatenated with raw SQL query can result in SQL Injection. In order to execute raw query safely, prepared statement should be used. SQLAlchemy provides TextualSQL to easily used prepared statement with named parameters. For complex SQL composition, use SQL Expression Language or Schema Definition Language. In most cases, SQLAlchemy ORM will be a better option. |

### astro-check (0 issues)
No issues found.

### svelte-check (0 issues)
No issues found.

### gitleaks (44 issues)
| File | Line | Code | Message |
|------|------|------|---------|
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/result.json | 58 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/result.json | 59 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/result.json | 80 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/result.json | 81 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 58 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 59 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 82 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 83 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 104 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 105 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 128 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 129 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 150 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 151 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 174 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 175 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 198 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 199 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 220 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 221 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 242 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 243 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 266 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 267 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 290 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 291 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 314 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 315 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 338 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 339 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 362 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 363 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 386 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 387 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 410 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 411 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 434 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 435 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 458 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 459 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 482 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 483 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 506 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |
| reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json | 507 |  | [generic-api-key] Detected a Generic API Key, potentially exposing access to various services and sensitive operations. [REDACTED] |

### mypy (0 issues)
No issues found.

### vue-tsc (0 issues)
No issues found.

### shellcheck (0 issues)
No issues found.

### bandit (543 issues)
| File | Line | Code | Message |
|------|------|------|---------|
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 32 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 33 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 42 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 43 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 44 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 53 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 63 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 64 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 65 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 74 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 75 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 80 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 85 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 94 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 95 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 100 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 101 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 118 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 125 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 130 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 136 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 144 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 152 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 161 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 162 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 163 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 164 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 185 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 186 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 206 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 207 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 228 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 230 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 251 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 254 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 273 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 293 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 294 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 258 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 259 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 264 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 265 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 270 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 275 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 276 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 281 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 282 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 287 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 293 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 298 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 303 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 316 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 323 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 329 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 330 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 334 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 354 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 360 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 368 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 370 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 376 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 378 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 380 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 389 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 390 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 398 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 407 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 455 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 456 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 459 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 462 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 466 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 470 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 474 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 479 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 492 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 493 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 494 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 495 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 496 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 497 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 502 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 503 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 508 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 509 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 510 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 515 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 516 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 533 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 538 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 539 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_bdd.py | 30 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_bdd.py | 37 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_bdd.py | 38 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_bdd.py | 53 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_bdd.py | 54 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_bdd.py | 69 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_bdd.py | 71 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_bdd.py | 72 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_bdd.py | 80 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_bdd.py | 87 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_bdd.py | 88 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_bdd.py | 89 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_bdd.py | 90 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_bdd.py | 91 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_bdd.py | 106 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 74 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 75 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 76 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 77 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 78 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 79 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 80 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 81 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 82 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 83 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 103 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 104 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 105 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 106 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 107 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 108 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 140 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 141 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_benchmark.py | 142 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_paths.py | 22 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_paths.py | 23 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_paths.py | 24 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_paths.py | 25 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_paths.py | 40 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_paths.py | 41 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_cli_paths.py | 42 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 30 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 36 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 42 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 46 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 48 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 58 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 68 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 70 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 76 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 80 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 93 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 102 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 108 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 114 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 118 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 16 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 17 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 23 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 24 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 29 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 35 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 40 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 44 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 52 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 59 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 68 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 74 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 76 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 80 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 87 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 88 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 89 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 90 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_detector.py | 23 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_detector.py | 35 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_detector.py | 47 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_detector.py | 59 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_detector.py | 71 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_detector.py | 83 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_detector.py | 96 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_detector.py | 108 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_detector.py | 122 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_detector.py | 135 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_detector.py | 154 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_detector.py | 161 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_detector.py | 171 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_detector.py | 178 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_elements.py | 51 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_elements.py | 108 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_elements.py | 110 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_elements.py | 117 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_elements.py | 122 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_elements.py | 126 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 54 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 55 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 66 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 67 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 73 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 85 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 104 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 105 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 111 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 131 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 140 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 154 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 164 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 174 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 175 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 190 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 191 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 50 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 56 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 62 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 70 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 83 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 84 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 85 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 86 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 92 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 99 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 113 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 116 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 129 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 139 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 140 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 141 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 142 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 152 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 153 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 154 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 159 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 165 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 177 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 182 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 183 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 188 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_graph.py | 189 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_html_reporter.py | 10 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_html_reporter.py | 16 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_html_reporter.py | 23 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_html_reporter.py | 30 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_inputs.py | 57 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_inputs.py | 62 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_inputs.py | 63 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_inputs.py | 68 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_inputs.py | 73 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_inputs.py | 78 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_inputs.py | 83 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_integration.py | 96 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_integration.py | 99 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_integration.py | 102 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 27 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 32 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 37 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 42 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 47 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 52 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 57 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 62 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 67 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 72 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 77 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 82 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 87 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 92 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 97 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 102 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 107 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 112 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 118 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 122 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 126 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 130 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_intent.py | 134 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 61 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 62 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 69 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 70 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 76 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 82 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 93 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 100 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 108 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 120 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 136 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 145 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 146 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 147 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 158 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 169 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 178 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 179 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 180 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 181 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 193 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 205 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_narrative.py | 206 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_navigator_confidence.py | 9 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_navigator_confidence.py | 10 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_navigator_confidence.py | 15 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_navigator_confidence.py | 16 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_navigator_confidence.py | 21 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 79 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 80 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 85 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 90 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 95 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 96 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 104 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 108 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 112 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 116 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 120 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 124 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 128 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 129 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 138 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 143 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 148 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 153 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 158 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 163 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 168 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 169 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 170 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 175 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 198 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 199 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 208 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 213 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 214 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 219 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 224 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 239 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 241 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 242 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 253 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 254 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 263 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 278 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 104 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 114 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 123 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 132 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 142 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 143 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 156 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 165 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 174 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 183 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 197 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 212 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 225 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 226 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 235 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 249 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 262 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 263 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 276 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 277 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 291 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 292 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 302 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 312 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 320 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_playwright_tests_codegen.py | 75 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_playwright_tests_codegen.py | 76 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_playwright_tests_codegen.py | 77 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_playwright_tests_codegen.py | 78 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_playwright_tests_codegen.py | 92 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_playwright_tests_codegen.py | 93 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_playwright_tests_codegen.py | 94 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_playwright_tests_codegen.py | 95 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_playwright_tests_codegen.py | 109 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_playwright_tests_codegen.py | 110 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_playwright_tests_codegen.py | 111 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_playwright_tests_codegen.py | 112 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_policy.py | 32 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_policy.py | 33 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_policy.py | 45 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_policy.py | 57 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_policy.py | 58 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_policy.py | 73 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_policy.py | 87 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 142 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 143 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 154 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 165 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 178 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 191 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 192 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 193 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 204 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 218 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 237 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 253 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 254 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 267 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 268 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 280 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 311 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 334 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 335 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 336 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 337 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 338 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 352 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 353 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 354 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 355 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 356 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 357 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 78 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 86 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 87 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 98 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 99 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 100 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 101 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 123 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 124 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 133 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 134 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 143 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 166 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 167 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 179 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 180 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 189 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenarios.py | 198 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 108 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 109 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 110 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 125 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 127 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 145 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 146 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 156 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 194 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 196 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 197 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 198 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 229 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 257 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 258 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 281 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 292 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 301 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 302 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 310 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 311 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 314 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 325 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 331 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 340 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 351 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 352 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 356 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 357 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 385 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 386 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 387 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 407 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 408 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 19 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 22 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 26 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 27 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 31 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 38 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 39 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 46 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 47 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 48 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 55 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 56 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 57 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 71 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 82 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 93 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 103 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 115 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 136 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 142 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 155 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 166 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 173 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 180 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 181 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 187 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 191 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 197 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 198 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 199 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 200 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_state.py | 201 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 32 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 38 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 46 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 54 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 60 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 66 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 72 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 78 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 84 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 90 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 96 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 102 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 108 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 114 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 120 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 126 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 132 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 138 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 144 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 150 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 156 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 162 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 168 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 172 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 176 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 182 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 192 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 193 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 194 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 202 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 203 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 211 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 212 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 216 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 225 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 226 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 227 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_verdict.py | 228 |  | [B101:assert_used] LOW severity, HIGH confidence: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/discovery/inputs.py | 80 |  | [B105:hardcoded_password_string] LOW severity, MEDIUM confidence: Possible hardcoded password: 'password' |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/reporting/html.py | 283 |  | [B105:hardcoded_password_string] LOW severity, MEDIUM confidence: Possible hardcoded password: '0' |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/analysis/narrative.py | 260 |  | [B608:hardcoded_sql_expressions] MEDIUM severity, LOW confidence: Possible SQL injection vector through string-based query construction. |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/analysis/narrative.py | 288 |  | [B608:hardcoded_sql_expressions] MEDIUM severity, LOW confidence: Possible SQL injection vector through string-based query construction. |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/analysis/narrative.py | 352 |  | [B608:hardcoded_sql_expressions] MEDIUM severity, LOW confidence: Possible SQL injection vector through string-based query construction. |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/analysis/narrative.py | 370 |  | [B608:hardcoded_sql_expressions] MEDIUM severity, LOW confidence: Possible SQL injection vector through string-based query construction. |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/discovery/intent.py | 66 |  | [B608:hardcoded_sql_expressions] MEDIUM severity, LOW confidence: Possible SQL injection vector through string-based query construction. |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/discovery/intent.py | 158 |  | [B608:hardcoded_sql_expressions] MEDIUM severity, LOW confidence: Possible SQL injection vector through string-based query construction. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_html_reporter.py | 9 |  | [B108:hardcoded_tmp_directory] MEDIUM severity, MEDIUM confidence: Probable insecure usage of temp file/directory. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_html_reporter.py | 14 |  | [B108:hardcoded_tmp_directory] MEDIUM severity, MEDIUM confidence: Probable insecure usage of temp file/directory. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_html_reporter.py | 20 |  | [B108:hardcoded_tmp_directory] MEDIUM severity, MEDIUM confidence: Probable insecure usage of temp file/directory. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_html_reporter.py | 27 |  | [B108:hardcoded_tmp_directory] MEDIUM severity, MEDIUM confidence: Probable insecure usage of temp file/directory. |
| /Users/eiteldagnin/Code/ui-framework/tests/test_html_reporter.py | 28 |  | [B108:hardcoded_tmp_directory] MEDIUM severity, MEDIUM confidence: Probable insecure usage of temp file/directory. |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/discovery/actions.py | 79 |  | [B324:hashlib] HIGH severity, HIGH confidence: Use of weak MD5 hash for security. Consider usedforsecurity=False |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/discovery/elements.py | 112 |  | [B324:hashlib] HIGH severity, HIGH confidence: Use of weak MD5 hash for security. Consider usedforsecurity=False |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/reporting/html.py | 124 |  | [B704:markupsafe_markup_xss] MEDIUM severity, HIGH confidence: Potential XSS with ``markupsafe.Markup`` detected. Do not use ``Markup`` on untrusted data. |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/reporting/html.py | 125 |  | [B704:markupsafe_markup_xss] MEDIUM severity, HIGH confidence: Potential XSS with ``markupsafe.Markup`` detected. Do not use ``Markup`` on untrusted data. |

### shfmt (0 issues)
No issues found.

### ruff (69 issues)
| File | Line | Code | Message |
|------|------|------|---------|
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 9 | F401 | `playwright.sync_api.Locator` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 9 | F401 | `playwright.sync_api.expect` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pom_tests.py | 8 | F401 | `pytest` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pom_tests.py | 9 | F401 | `playwright.sync_api.expect` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pom_tests.py | 12 | F811 | Redefinition of unused `SearchResultsPage` from line 11: `SearchResultsPage` redefined here |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pom_tests.py | 13 | F811 | Redefinition of unused `SearchResultsPage` from line 12: `SearchResultsPage` redefined here |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pom_tests.py | 14 | F811 | Redefinition of unused `SearchResultsPage` from line 13: `SearchResultsPage` redefined here |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pom_tests.py | 15 | F811 | Redefinition of unused `SearchResultsPage` from line 14: `SearchResultsPage` redefined here |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/scenario_tests.py | 9 | F401 | `pytest` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/landing_page.py | 9 | F401 | `playwright.sync_api.Locator` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/landing_page.py | 9 | F401 | `playwright.sync_api.expect` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 9 | F401 | `playwright.sync_api.Locator` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 9 | F401 | `playwright.sync_api.expect` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/pom_tests.py | 8 | F401 | `pytest` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/pom_tests.py | 9 | F401 | `playwright.sync_api.expect` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/pom_tests.py | 11 | F401 | `pages.landing_page.LandingPage` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/tests.py | 13 | F401 | `re` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/tests.py | 15 | F401 | `pytest` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/pom_tests.py | 8 | F401 | `pytest` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/pom_tests.py | 9 | F401 | `playwright.sync_api.expect` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/pom_tests.py | 12 | F811 | Redefinition of unused `SearchResultsPage` from line 11: `SearchResultsPage` redefined here |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/pom_tests.py | 13 | F811 | Redefinition of unused `SearchResultsPage` from line 12: `SearchResultsPage` redefined here |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/pom_tests.py | 14 | F811 | Redefinition of unused `SearchResultsPage` from line 13: `SearchResultsPage` redefined here |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/pom_tests.py | 15 | F811 | Redefinition of unused `SearchResultsPage` from line 14: `SearchResultsPage` redefined here |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 15 | F401 | `pytest` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/scenario_tests.py | 9 | F401 | `pytest` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 9 | F401 | `flowscout.analysis.archetype.CatalogEntry` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 12 | F401 | `flowscout.analysis.archetype.PageCatalog` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/tests/test_bdd.py | 70 | E741 | Ambiguous variable name: `l` |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 5 | F401 | `pytest` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/tests/test_coverage.py | 5 | F401 | `pytest` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/tests/test_expectations.py | 5 | F401 | `pytest` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 8 | F401 | `pytest` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 5 | F401 | `unittest.mock.patch` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 10 | F401 | `flowscout.analysis.archetype.ContentDensity` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 11 | F401 | `flowscout.analysis.archetype.PageAnalysis` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 13 | F401 | `flowscout.analysis.archetype.RepeatedStructure` imported but unused |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pages/search_results_page.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/pom_tests.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/scenario_tests.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/reports/2026/02.February/07-02-2026/22.29.41/tests.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/landing_page.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/pages/search_results_page.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/pom_tests.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/tests.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/pom_tests.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/tests.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/reports/debs-obrien.github.io/baseline/scenario_tests.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/analysis/archetype.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/analysis/expectations.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/analysis/site_model.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/page_objects.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/pom_tests.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/codegen/scenario_tests.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/core/browser.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/core/navigator.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/core/state.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/discovery/elements.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/reporting/html.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/reporting/terminal.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/src/flowscout/storage/db.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/tests/test_actions.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/tests/test_archetype.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/tests/test_context.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/tests/test_integration.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/tests/test_page_objects.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/tests/test_planner.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/tests/test_scenario_tests_codegen.py | 0 | FORMAT | Would reformat file |
| /Users/eiteldagnin/Code/ui-framework/tests/test_site_model.py | 0 | FORMAT | Would reformat file |

### oxlint (6 issues)
| File | Line | Code | Message |
|------|------|------|---------|
| src/flowscout/js/dom_structure.ts | 1 | eslint(no-unused-expressions) | Expected expression to be used |
| src/flowscout/js/visible_text.ts | 1 | eslint(no-unused-expressions) | Expected expression to be used |
| src/flowscout/js/signals.ts | 1 | eslint(no-unused-expressions) | Expected expression to be used |
| src/flowscout/js/keyboard_hints.ts | 1 | eslint(no-unused-expressions) | Expected expression to be used |
| src/flowscout/js/discovery.ts | 1 | eslint(no-unused-expressions) | Expected expression to be used |
| src/flowscout/js/form_state.ts | 1 | eslint(no-unused-expressions) | Expected expression to be used |

### cargo_deny (0 issues)
No issues found.

### yamllint (0 issues)
No issues found.

### rustfmt (0 issues)
No issues found.

### tsc (216 issues)
| File | Line | Code | Message |
|------|------|------|---------|
| report-ui/src/App.tsx | 3 | TS6142 | Module './components/CommandBar' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/CommandBar.tsx', but '--jsx' is not set. |
| report-ui/src/App.tsx | 4 | TS6142 | Module './components/JourneyDetailPanel' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/JourneyDetailPanel.tsx', but '--jsx' is not set. |
| report-ui/src/App.tsx | 5 | TS6142 | Module './components/JourneyList' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/JourneyList.tsx', but '--jsx' is not set. |
| report-ui/src/App.tsx | 6 | TS6142 | Module './components/OutcomePanel' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/OutcomePanel.tsx', but '--jsx' is not set. |
| report-ui/src/App.tsx | 7 | TS6142 | Module './components/PageReference' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/PageReference.tsx', but '--jsx' is not set. |
| report-ui/src/App.tsx | 8 | TS6142 | Module './components/StateGraph' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/StateGraph.tsx', but '--jsx' is not set. |
| report-ui/src/App.tsx | 9 | TS6142 | Module './components/StatsSummary' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/StatsSummary.tsx', but '--jsx' is not set. |
| report-ui/src/App.tsx | 74 | TS2802 | Type 'Set<string>' can only be iterated through when using the '--downlevelIteration' flag or with a '--target' of 'es2015' or higher. |
| report-ui/src/App.tsx | 212 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/App.tsx | 214 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/App.tsx | 216 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/App.tsx | 229 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/App.tsx | 231 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/App.tsx | 232 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/App.tsx | 242 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/App.tsx | 244 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/App.tsx | 258 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/App.tsx | 260 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/App.tsx | 264 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/App.tsx | 266 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/App.tsx | 267 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/App.tsx | 276 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/App.tsx | 277 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/App.tsx | 278 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/App.tsx | 286 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 14 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 15 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 16 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 17 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 18 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 19 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 20 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 21 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 22 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 23 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 24 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 25 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 34 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 35 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 36 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 37 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 40 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 41 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 46 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 51 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 52 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 53 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 61 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 75 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/CommandBar.tsx | 76 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 6 | TS6142 | Module './StepTimeline' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/StepTimeline.tsx', but '--jsx' is not set. |
| report-ui/src/components/JourneyDetailPanel.tsx | 48 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 50 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 51 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 52 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 53 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 61 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 66 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 67 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 68 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 69 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 70 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 72 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 73 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 77 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 87 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 88 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyDetailPanel.tsx | 91 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyList.tsx | 4 | TS6142 | Module './JourneyRow' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/JourneyRow.tsx', but '--jsx' is not set. |
| report-ui/src/components/JourneyList.tsx | 20 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyList.tsx | 21 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyList.tsx | 22 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyList.tsx | 25 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyList.tsx | 28 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyList.tsx | 30 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyList.tsx | 43 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyList.tsx | 49 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyList.tsx | 50 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyRow.tsx | 15 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyRow.tsx | 16 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyRow.tsx | 24 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyRow.tsx | 34 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyRow.tsx | 40 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyRow.tsx | 41 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyRow.tsx | 42 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyRow.tsx | 54 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyRow.tsx | 55 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyRow.tsx | 72 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyRow.tsx | 81 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyRow.tsx | 83 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyRow.tsx | 84 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyRow.tsx | 85 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyRow.tsx | 91 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/JourneyRow.tsx | 111 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/OutcomePanel.tsx | 19 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/OutcomePanel.tsx | 20 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/OutcomePanel.tsx | 25 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/OutcomePanel.tsx | 29 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/OutcomePanel.tsx | 30 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/OutcomePanel.tsx | 31 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/OutcomePanel.tsx | 32 | TS2550 | Property 'replaceAll' does not exist on type 'string'. Do you need to change your target library? Try changing the 'lib' compiler option to 'es2021' or later. |
| report-ui/src/components/OutcomePanel.tsx | 34 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/OutcomePanel.tsx | 36 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/OutcomePanel.tsx | 37 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/OutcomePanel.tsx | 46 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/OutcomePanel.tsx | 51 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/OutcomePanel.tsx | 53 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/OutcomePanel.tsx | 65 | TS2550 | Property 'replaceAll' does not exist on type 'string'. Do you need to change your target library? Try changing the 'lib' compiler option to 'es2021' or later. |
| report-ui/src/components/OutcomePanel.tsx | 71 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/OutcomePanel.tsx | 73 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/OutcomePanel.tsx | 91 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/OutcomePanel.tsx | 100 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/PageReference.tsx | 15 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/PageReference.tsx | 16 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/PageReference.tsx | 19 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/PageReference.tsx | 21 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/PageReference.tsx | 25 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/PageReference.tsx | 28 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/PageReference.tsx | 29 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/PageReference.tsx | 30 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/PageReference.tsx | 35 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 26 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 34 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 35 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 36 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 37 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 38 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 39 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 40 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 42 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 43 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 44 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 45 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 177 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 178 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 179 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 182 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 186 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 187 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 188 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 190 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StateGraph.tsx | 191 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 15 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 16 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 19 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 20 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 21 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 40 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 41 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 44 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 45 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 46 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 47 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 48 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 50 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 51 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 52 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 53 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 54 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 55 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 59 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 60 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 61 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 66 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 67 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StatsSummary.tsx | 68 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimeline.tsx | 2 | TS6142 | Module './StepTimelineNode' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/StepTimelineNode.tsx', but '--jsx' is not set. |
| report-ui/src/components/StepTimeline.tsx | 11 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimeline.tsx | 12 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimeline.tsx | 16 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimeline.tsx | 24 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimeline.tsx | 33 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimeline.tsx | 35 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimeline.tsx | 37 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimeline.tsx | 39 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimeline.tsx | 40 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimeline.tsx | 42 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimeline.tsx | 43 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimeline.tsx | 44 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimeline.tsx | 45 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimeline.tsx | 52 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 13 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 14 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 18 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 33 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 35 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 38 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 39 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 42 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 43 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 44 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 47 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 50 | TS2550 | Property 'replaceAll' does not exist on type 'string'. Do you need to change your target library? Try changing the 'lib' compiler option to 'es2021' or later. |
| report-ui/src/components/StepTimelineNode.tsx | 54 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 55 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 56 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 58 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 59 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 62 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 67 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 73 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 75 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 76 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 81 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 82 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 87 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 97 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 109 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/components/StepTimelineNode.tsx | 110 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/main.tsx | 4 | TS5097 | An import path can only end with a '.tsx' extension when 'allowImportingTsExtensions' is enabled. |
| report-ui/src/main.tsx | 4 | TS6142 | Module './App.tsx' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/App.tsx', but '--jsx' is not set. |
| report-ui/src/main.tsx | 7 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/src/main.tsx | 8 | TS17004 | Cannot use JSX unless the '--jsx' flag is provided. |
| report-ui/vite.config.ts | 2 | TS2307 | Cannot find module '@vitejs/plugin-react' or its corresponding type declarations. |
| report-ui/vite.config.ts | 3 | TS2307 | Cannot find module '@tailwindcss/vite' or its corresponding type declarations. |
| src/flowscout/js/keyboard_hints.ts | 24 | TS2802 | Type 'Set<string>' can only be iterated through when using the '--downlevelIteration' flag or with a '--target' of 'es2015' or higher. |

### hadolint (0 issues)
No issues found.

### taplo (1 issues)
| File | Line | Code | Message |
|------|------|------|---------|
| /Users/eiteldagnin/Code/ui-framework/pyproject.toml | 0 | format | the file is not properly formatted |

### pydoclint (0 issues)
No issues found.

### cargo_audit (0 issues)
No issues found.
