"""Data models for Todo application."""

from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    """Enumeration for task completion status."""

    PENDING = "Pending"
    COMPLETED = "Completed"


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique integer identifier (auto-generated, immutable)
        title: Task title (required, non-empty)
        description: Task description (optional)
        status: Current completion status (PENDING or COMPLETED)
    """

    id: int
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
