from __future__ import annotations

from typing import List

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--compliance-check",
        action="store_true",
        default=False,
        help="Run OpenTSR compliance test suite",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "compliance: OpenTSR requirement compliance checks")


def pytest_collection_modifyitems(config: pytest.Config, items: List[pytest.Item]) -> None:
    if config.getoption("--compliance-check"):
        return

    skip_compliance = pytest.mark.skip(reason="use --compliance-check to run compliance suite")
    for item in items:
        if "compliance" in item.keywords:
            item.add_marker(skip_compliance)
