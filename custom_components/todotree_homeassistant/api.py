"""Todotree client wrapper using local Python API (no HTTP)."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

from todotree import Config, TaskManager
from todotree.Commands.Add import Add
from todotree.Commands.Do import Do

if TYPE_CHECKING:
    from todotree.Task.Task import Task


class TodotreeApiClientError(Exception):
    """General client error."""


class TodotreeApiClientCommunicationError(TodotreeApiClientError):
    """Unused placeholder - kept for coordinator patterns."""


class TodotreeApiClientAuthError(TodotreeApiClientError):
    """Unused (no auth) - kept for flow compatibility."""


@dataclass(frozen=True)
class TaskRecord:
    """Lightweight representation of a todotree task."""

    number: int
    text: str
    due: date | None


class TodotreeApiClient:
    """Thin wrapper around todotree Config + TaskManager + Commands."""

    def __init__(self, data_path: str | None = None) -> None:
        """Initialize with optional path to todotree config/data folder."""
        self._data_path = Path(data_path).expanduser() if data_path else None

    def _load_config(self) -> Config:
        """Load todotree Config from path or XDG defaults."""
        cfg = Config()
        if self._data_path is None:
            cfg.read()  # XDG defaults
            return cfg
        if self._data_path.is_dir():
            config_file = self._data_path / "config.yaml"
        else:
            config_file = self._data_path
        cfg.read(config_file)
        return cfg

    def _load_manager(self, cfg: Config) -> TaskManager:
        """Create TaskManager and import tasks from files."""
        mgr = TaskManager(cfg)
        mgr.import_tasks()
        return mgr

    async def async_validate(self) -> None:
        """Validate config can be read and tasks imported."""

        def _validate() -> None:
            cfg = self._load_config()
            _ = self._load_manager(cfg)

        await asyncio.to_thread(_validate)

    async def async_list_tasks(self) -> list[TaskRecord]:
        """Return active tasks filtered by blocks and threshold dates."""

        def _list() -> list[TaskRecord]:
            cfg = self._load_config()
            mgr = self._load_manager(cfg)
            mgr.filter_block()
            mgr.filter_t_date()
            return [
                TaskRecord(
                    number=t.i,
                    text=t.task_string.strip(),
                    due=t.due_date,
                )
                for t in mgr.task_list
            ]

        return await asyncio.to_thread(_list)

    async def async_add_task(
        self, text: str, due: date | None = None
    ) -> TaskRecord:
        """Add new task and commit+push."""

        def _add() -> TaskRecord:
            cfg = self._load_config()
            mgr = self._load_manager(cfg)
            parts = [text]
            if due:
                parts.append(f"due:{due.isoformat()}")
            add_cmd = Add(cfg, mgr)
            task = add_cmd(" ".join(parts))
            cfg.git.commit_and_push("add")
            return TaskRecord(
                number=task.i,
                text=task.task_string.strip(),
                due=task.due_date,
            )

        return await asyncio.to_thread(_add)

    async def async_complete_tasks(self, numbers: Iterable[int]) -> None:
        """Mark tasks done and commit+push."""

        def _do() -> None:
            cfg = self._load_config()
            mgr = self._load_manager(cfg)
            do_cmd = Do(cfg, mgr)
            _ = do_cmd(list(numbers))
            cfg.git.commit_and_push("do")

        await asyncio.to_thread(_do)

    async def async_set_due(
        self, number: int, new_due: date | None
    ) -> TaskRecord:
        """Update due date on a task and commit+push."""

        def _set() -> TaskRecord:
            cfg = self._load_config()
            mgr = self._load_manager(cfg)

            def _update_due(task: Task, dt: datetime | None) -> None:
                if dt is not None:
                    task.add_or_update_due(dt)

            dt = (
                datetime.combine(new_due, datetime.min.time())
                if new_due
                else None
            )
            updated = mgr.add_or_update_task(number, _update_due, dt)
            cfg.git.commit_and_push("update-due")
            return TaskRecord(
                number=updated.i,
                text=updated.task_string.strip(),
                due=updated.due_date,
            )

        return await asyncio.to_thread(_set)

    async def async_append_description(
        self, number: int, extra: str
    ) -> TaskRecord:
        """Append text to task and commit+push."""

        def _append() -> TaskRecord:
            cfg = self._load_config()
            mgr = self._load_manager(cfg)
            mgr.append_to_task(number, f" {extra}")
            cfg.git.commit_and_push("append")
            mgr.import_tasks()
            t = next(
                (x for x in mgr.task_list if x.i == number), None
            )
            if t is None:
                msg = f"Task {number} not found after append"
                raise TodotreeApiClientError(msg)
            return TaskRecord(
                number=t.i,
                text=t.task_string.strip(),
                due=t.due_date,
            )

        return await asyncio.to_thread(_append)
