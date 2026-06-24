"""Todotree entity base class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import TodotreeUpdateCoordinator


class TodotreeEntity(CoordinatorEntity[TodotreeUpdateCoordinator]):
    """Base entity for Todotree."""

    def __init__(self, coordinator: TodotreeUpdateCoordinator) -> None:
        """Initialize base entity with device info and unique id."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    coordinator.config_entry.domain,
                    coordinator.config_entry.entry_id,
                )
            },
            name="Todotree",
            manufacturer="Todotree",
            model="Task list",
        )
