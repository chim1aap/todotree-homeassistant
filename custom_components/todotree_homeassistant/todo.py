"""Todo platform for Todotree."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.todo import (
    TodoItem,
    TodoItemStatus,
    TodoListEntity,
    TodoListEntityFeature,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import TodotreeUpdateCoordinator

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .api import TaskRecord


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the todo platform for a config entry."""
    coordinator: TodotreeUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([TodotreeTodoEntity(coordinator)], update_before_add=True)


class TodotreeTodoEntity(CoordinatorEntity[TodotreeUpdateCoordinator], TodoListEntity):
    """Todotree task list as a TodoListEntity."""

    _attr_supported_features = (
        TodoListEntityFeature.CREATE_TODO_ITEM
        | TodoListEntityFeature.UPDATE_TODO_ITEM
        | TodoListEntityFeature.DELETE_TODO_ITEM
        | TodoListEntityFeature.SET_DESCRIPTION_ON_ITEM
        | TodoListEntityFeature.SET_DUE_DATE_ON_ITEM
        | TodoListEntityFeature.SET_DUE_DATETIME_ON_ITEM
    )

    _attr_name = "Todotree"

    def __init__(self, coordinator: TodotreeUpdateCoordinator) -> None:
        """Initialize entity bound to coordinator."""
        super().__init__(coordinator)
        self._items: list[TodoItem] = []

    @property
    def todo_items(self) -> list[TodoItem]:
        """Return current todo items."""
        return self._items

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update internal cache from coordinator data and write state."""
        data = self.coordinator.data or []
        self._items = [self._record_to_item(rec) for rec in data]
        self.async_write_ha_state()

    async def async_create_todo_item(self, item: TodoItem) -> None:
        """Create task in todotree and refresh list."""
        await self.coordinator.client.async_add_task(text=item.summary, due=item.due)
        await self.coordinator.async_request_refresh()

    async def async_update_todo_item(self, item: TodoItem) -> None:
        """Update due/description on a task and refresh list."""
        if not item.uid:
            return
        num = int(item.uid)
        if item.due is not None:
            await self.coordinator.client.async_set_due(num, item.due)
        if item.description:
            await self.coordinator.client.async_append_description(
                num, item.description
            )
        await self.coordinator.async_request_refresh()

    async def async_delete_todo_items(self, uids: list[str]) -> None:
        """Mark tasks done and refresh list."""
        numbers = [int(uid) for uid in uids]
        await self.coordinator.client.async_complete_tasks(numbers)
        await self.coordinator.async_request_refresh()

    def _record_to_item(self, rec: TaskRecord) -> TodoItem:
        """Map TaskRecord to Home Assistant TodoItem."""
        return TodoItem(
            uid=str(rec.number),
            summary=rec.text,
            status=TodoItemStatus.NEEDS_ACTION,
            due=rec.due,
        )
