"""JUnit XML export for CI/CD integration."""

from __future__ import annotations

import xml.etree.ElementTree as ET  # nosec B405 - generating XML, not parsing untrusted input
from pathlib import Path
from xml.dom import minidom  # nosec B408 - generating XML, not parsing untrusted input

from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.discovery.actions import OutcomeType


def generate_junit_report(result: ExplorationResult, output_path: str) -> None:
    """Generate a JUnit XML report from an exploration result."""
    root = _build_junit_xml(result)
    xml_str = _prettify(root)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(xml_str)


def _build_junit_xml(result: ExplorationResult) -> ET.Element:
    """Build a JUnit XML element tree from an exploration result."""
    testsuites = ET.Element("testsuites")
    testsuites.set("name", "flowscout")
    testsuites.set("time", str(round(result.duration_seconds, 2)))

    # Group flows by category
    categories: dict[str, list[Flow]] = {}
    for flow in result.flows:
        cat = flow.category or "Other"
        categories.setdefault(cat, []).append(flow)

    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0

    for cat_name, flows in categories.items():
        testsuite = ET.SubElement(testsuites, "testsuite")
        testsuite.set("name", cat_name)
        testsuite.set("tests", str(len(flows)))

        suite_failures = 0
        suite_errors = 0
        suite_skipped = 0

        for flow in flows:
            testcase = ET.SubElement(testsuite, "testcase")
            testcase.set("name", flow.name)
            testcase.set("classname", f"flowscout.{cat_name}")

            has_severe = any(
                outcome
                in {
                    OutcomeType.NETWORK_ERROR,
                    OutcomeType.TIMEOUT,
                    OutcomeType.EXCEPTION,
                }
                for outcome in flow.outcomes
            )
            verdict_val = (
                "pass" if flow.is_stable else ("fail" if has_severe else "warn")
            )

            if verdict_val == "fail":
                failure = ET.SubElement(testcase, "failure")
                failure.set("message", "Unstable flow with severe failure outcomes")
                failure.set("type", "AssertionError")
                if flow.narrative and flow.narrative.conclusion:
                    failure.text = flow.narrative.conclusion
                suite_failures += 1
            elif verdict_val == "warn":
                error = ET.SubElement(testcase, "error")
                error.set("message", "Unstable flow")
                error.set("type", "Warning")
                suite_errors += 1
            elif not verdict_val:
                skipped = ET.SubElement(testcase, "skipped")
                skipped.set("message", "No stability signal")
                suite_skipped += 1

        testsuite.set("failures", str(suite_failures))
        testsuite.set("errors", str(suite_errors))
        testsuite.set("skipped", str(suite_skipped))

        total_tests += len(flows)
        total_failures += suite_failures
        total_errors += suite_errors
        total_skipped += suite_skipped

    testsuites.set("tests", str(total_tests))
    testsuites.set("failures", str(total_failures))
    testsuites.set("errors", str(total_errors))

    return testsuites


def _prettify(element: ET.Element) -> str:
    """Return a pretty-printed XML string."""
    rough = ET.tostring(element, encoding="unicode", xml_declaration=True)
    parsed = minidom.parseString(rough)  # nosec B318 - parsing our own generated XML
    return parsed.toprettyxml(indent="  ")
