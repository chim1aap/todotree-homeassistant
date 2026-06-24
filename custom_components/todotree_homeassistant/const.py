"""Constants for the Todotree integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "todotree_homeassistant"

CONF_DATA_PATH = "data_path"
CONF_GIT_MODE = "git_mode"

DEFAULT_SCAN_INTERVAL = 300  # 5 minutes
