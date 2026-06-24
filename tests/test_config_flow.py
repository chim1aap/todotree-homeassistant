"""Tests for Todotree config flow."""

from pathlib import Path

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.todotree_homeassistant.const import CONF_DATA_PATH, DOMAIN


@pytest.mark.asyncio
async def test_config_flow_valid(tmp_path: Path, hass: HomeAssistant) -> None:
    """Config flow accepts valid data folder and creates entry."""
    config_dir = tmp_path / "todotree"
    config_dir.mkdir()
    (config_dir / "config.yaml").write_text(
        """
paths:
  folder: "{folder}"
  todo_file: "{folder}/todo.txt"
  done_file: "{folder}/done.txt"
  recur_file: "{folder}/recur.txt"
  stale_file: "{folder}/stale.txt"
""".format(folder=str(config_dir).replace("\\", "/"))
    )
    for name in ["todo.txt", "done.txt", "recur.txt", "stale.txt"]:
        (config_dir / name).write_text("")

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )
    assert result["type"] == FlowResultType.FORM

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input={CONF_DATA_PATH: str(config_dir)}
    )
    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Todotree"
    assert result2["data"][CONF_DATA_PATH] == str(config_dir)
