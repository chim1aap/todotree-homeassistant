"""Pytest fixtures for Todotree integration tests."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(_enable_custom_integrations: None) -> None:
    """Enable custom integrations in HA test harness."""
    return
