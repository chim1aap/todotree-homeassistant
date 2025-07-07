"""Custom types for custom_components/TodoTree."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import TodotreeApiClient
    from .coordinator import TodotreeUpdateCoordinator


type TodotreeConfigEntry = ConfigEntry[TodotreeData]


@dataclass
class TodotreeData:
    """Data for the Todotree integration."""

    client: TodotreeApiClient
    coordinator: TodotreeUpdateCoordinator
    integration: Integration
