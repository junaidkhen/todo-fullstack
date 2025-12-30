"""Input validation utilities for Todo application."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import Task


def validate_title(title: str) -> str:
    """Validate and normalize task title.

    Args:
        title: User-provided title string

    Returns:
        Cleaned title string (whitespace stripped)

    Raises:
        ValueError: If title is empty or contains only whitespace
    """
    cleaned = title.strip()
    if not cleaned:
        raise ValueError("Title cannot be empty")
    return cleaned


def validate_task_id(task_id: str, tasks: list["Task"]) -> int:
    """Validate task ID input and check existence.

    Args:
        task_id: User-provided task ID as string
        tasks: List of existing tasks to check against

    Returns:
        Validated task ID as integer

    Raises:
        ValueError: If ID format is invalid or task not found
    """
    # Check numeric format
    if not task_id.strip().isdigit():
        raise ValueError(f"Invalid task ID format: '{task_id}'")

    # Convert to integer
    id_num = int(task_id.strip())

    # Check existence
    if not any(t.id == id_num for t in tasks):
        raise ValueError(f"Task with ID {id_num} not found")

    return id_num
