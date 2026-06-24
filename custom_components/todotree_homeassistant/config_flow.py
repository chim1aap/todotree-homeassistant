"""Config flow for the Todotree integration."""

from __future__ import annotations

from pathlib import Path

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector

from .api import TodotreeApiClient, TodotreeApiClientError
from .const import CONF_DATA_PATH, DOMAIN, LOGGER


class TodotreeConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Todotree."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        errors: dict[str, str] = {}
        if user_input is not None:
            data_path = user_input[CONF_DATA_PATH]
            try:
                client = TodotreeApiClient(data_path=data_path)
                await client.async_validate()
            except FileNotFoundError:
                errors["base"] = "path_not_found"
            except TodotreeApiClientError as exc:
                LOGGER.exception("Unexpected error validating todotree path: %s", exc)
                errors["base"] = "unknown"
            except Exception as exc:  # noqa: BLE001
                LOGGER.exception("Unexpected error: %s", exc)
                errors["base"] = "unknown"
            else:
                # Use resolved absolute path as unique id (one entry per folder)
                resolved = str(Path(data_path).expanduser().resolve())
                await self.async_set_unique_id(resolved)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title="Todotree",
                    data={CONF_DATA_PATH: data_path},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_DATA_PATH,
                        default=(user_input or {}).get(CONF_DATA_PATH, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                },
            ),
            errors=errors,
        )
