"""Tests for setup and todo entity behavior."""

from pathlib import Path

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from custom_components.todotree_homeassistant.const import CONF_DATA_PATH, DOMAIN


@pytest.mark.asyncio
async def test_setup_and_todo_entity(tmp_path: Path, hass: HomeAssistant) -> None:
    """Setup entry and ensure todo entity is created."""
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

    entry = await hass.config_entries.async_add(
        hass.config_entries.async_create_entry(
            title="Todotree", data={CONF_DATA_PATH: str(config_dir)}, domain=DOMAIN
        )
    )

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    erc = er.async_get(hass)
    entities = [
        e for e in erc.entities.values() if e.domain == "todo" and e.platform == DOMAIN
    ]
    assert entities, "Todo entity not created"
