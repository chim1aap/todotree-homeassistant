"""A todo platform for todotree"""

import asyncio
from typing import cast

from homeassistant.components.todo import (
    TodoItem,
    TodoItemStatus,
    TodoListEntity,
    TodoListEntityFeature,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, TASK_STATUS_PROPERTY, TASK_DESCRIPTION_PROPERTY, TASK_DATE_PROPERTY
from .coordinator import TodotreeUpdateCoordinator
from .notion_property_helper import NotionPropertyHelper as propHelper


async def async_setup_entry(
        hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the todotree platform config entry."""
    coordinator: TodotreeUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = ['Notion']
    async_add_entities(
        NotionTodoListEntity(coordinator, e)
        for e in entities
    )


class NotionTodoListEntity(CoordinatorEntity[TodotreeUpdateCoordinator], TodoListEntity):
    """A Notion TodoListEntity."""

    _attr_supported_features = (
            TodoListEntityFeature.CREATE_TODO_ITEM
            | TodoListEntityFeature.UPDATE_TODO_ITEM
            | TodoListEntityFeature.DELETE_TODO_ITEM
            | TodoListEntityFeature.SET_DESCRIPTION_ON_ITEM
            | TodoListEntityFeature.SET_DUE_DATE_ON_ITEM
            | TodoListEntityFeature.SET_DUE_DATETIME_ON_ITEM
    )

    def __init__(
            self,
            coordinator: TodotreeUpdateCoordinator,
            user: str,
    ) -> None:
        """Initialize TodoListEntity."""
        # TODO: Implement.
        super().__init__(coordinator=coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        raise NotImplemented("This method must be implemented.")

    async def async_create_todo_item(self, item: TodoItem) -> None:
        """Create a To-do item."""
        raise NotImplemented("This method must be implemented.")

    async def async_update_todo_item(self, item: TodoItem) -> None:
        """Update a To-do item."""
        raise NotImplemented("This method must be implemented.")

    async def async_delete_todo_items(self, uids: list[str]) -> None:
        """'Delete' a To-do item, aka move to done.txt"""
        raise NotImplemented("This method must be implemented.")

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass update state from existing coordinator data."""
        await super().async_added_to_hass()
        self._handle_coordinator_update()
