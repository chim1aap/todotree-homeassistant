"""Todo platform for Todotree."""

from __future__ import annotations

from datetime import date
from typing import Iterable

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

from .api import TaskRecord
from .const import DOMAIN
from .coordinator import TodotreeUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: TodotreeUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([TodotreeTodoEntity(coordinator)], True)


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
        super().__init__(coordinator)
        self._items: list[TodoItem] = []

    @property
    def todo_items(self) -> list[TodoItem]:
        return self._items

    @callback
    def _handle_coordinator_update(self) -> None:
        self._items = [self._record_to_item(rec) for rec in (self.coordinator.data or [])]
        self.async_write_ha_state()

    async def async_create_todo_item(self, item: TodoItem) -> None:
        text = item.summary
        due = item.due
        new_rec = await self.coordinator.client.async_add_task(text=text, due=due)
        await self.coordinator.async_request_refresh()

    async def async_update_todo_item(self, item: TodoItem) -> None:
        # Map to set due / append description depending on changed fields
        if not item.uid:
            return
        num = int(item.uid)
        if item.due is not None:
            await self.coordinator.client.async_set_due(num, item.due)
        if item.description:
            await self.coordinator.client.async_append_description(num, item.description)
        await self.coordinator.async_request_refresh()

    async def async_delete_todo_items(self, uids: list[str]) -> None:
        # Mark tasks done
        numbers = [int(uid) for uid in uids]
        await self.coordinator.client.async_complete_tasks(numbers)
        await self.coordinator.async_request_refresh()

    def _record_to_item(self, rec: TaskRecord) -> TodoItem:
        return TodoItem(
            uid=str(rec.number),
            summary=rec.text,
            status=TodoItemStatus.NEEDS_ACTION,
            due=rec.due,
        )
