"""DataUpdateCoordinator for TodoTree."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER
from .api import (
    TodotreeApiClientAuthError,
    TodotreeApiClientError, TodotreeApiClient,
)

if TYPE_CHECKING:
    from .data import TodotreeConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class TodotreeUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: TodotreeConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        client: TodotreeApiClient,
    ) -> None:
        """Initialize."""
        self.client = client
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            return await self.config_entry.runtime_data.client.async_get_data()
        except TodotreeApiClientAuthError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except TodotreeApiClientError as exception:
            raise UpdateFailed(exception) from exception
