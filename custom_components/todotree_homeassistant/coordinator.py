"""DataUpdateCoordinator for Todotree."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import TaskRecord, TodotreeApiClient, TodotreeApiClientError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN, LOGGER

if TYPE_CHECKING:
    from .data import TodotreeConfigEntry


class TodotreeUpdateCoordinator(DataUpdateCoordinator[list[TaskRecord]]):
    """Polls todotree task list periodically."""

    config_entry: TodotreeConfigEntry

    def __init__(self, hass: HomeAssistant, client: TodotreeApiClient) -> None:
        """Initialize coordinator with client."""
        self.client = client
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> list[TaskRecord]:
        """Fetch tasks from todotree."""
        try:
            return await self.client.async_list_tasks()
        except TodotreeApiClientError as exc:
            msg = f"Error fetching todotree tasks: {exc}"
            raise UpdateFailed(msg) from exc
        except Exception as exc:
            msg = f"Unexpected error: {exc}"
            raise UpdateFailed(msg) from exc
