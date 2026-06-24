"""Todotree integration setup."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.loader import async_get_loaded_integration

from .api import TodotreeApiClient
from .const import CONF_DATA_PATH, DOMAIN
from .coordinator import TodotreeUpdateCoordinator
from .data import TodotreeData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from .data import TodotreeConfigEntry

PLATFORMS: list[Platform] = [Platform.TODO]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TodotreeConfigEntry,
) -> bool:
    """Set up Todotree from a config entry."""
    client = TodotreeApiClient(data_path=entry.data[CONF_DATA_PATH])
    coordinator = TodotreeUpdateCoordinator(hass=hass, client=client)

    entry.runtime_data = TodotreeData(
        client=client,
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # Store for platforms expecting hass.data mapping
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: TodotreeConfigEntry,
) -> bool:
    """Unload Todotree entry."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return unloaded


async def async_reload_entry(
    hass: HomeAssistant,
    entry: TodotreeConfigEntry,
) -> None:
    await hass.config_entries.async_reload(entry.entry_id)
