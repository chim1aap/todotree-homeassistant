import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):  # noqa: PT005
    yield
