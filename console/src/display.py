"""Output formatting utilities for Todo application."""

from models import Task, TaskStatus


def truncate(text: str, max_length: int = 50) -> str:
    """Truncate text to maximum length with ellipsis indicator.

    Args:
        text: Text to truncate
        max_length: Maximum length (default: 50)

    Returns:
        Truncated text with "..." if longer than max_length
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def format_task_row(task: Task) -> str:
    """Format a single task as a table row.

    Args:
        task: Task object to format

    Returns:
        Formatted string row for the task
    """
    # Status indicator
    if task.status == TaskStatus.PENDING:
        status_str = "[ ] Pend."
    else:
        status_str = "[✓] Comp."

    # Truncate title and description for display
    title_display = truncate(task.title, 25)
    desc_display = truncate(task.description, 50) if task.description else ""

    # Format row with fixed-width columns
    return f"{task.id:>3} | {title_display:<25} | {status_str:<10} | {desc_display}"


def format_task_table(tasks: list[Task]) -> str:
    """Format list of tasks as ASCII table.

    Args:
        tasks: List of Task objects

    Returns:
        Formatted table string with header and rows
    """
    # Table header
    lines = []
    lines.append("ID | Title                     | Status     | Description")
    lines.append("---+---------------------------+------------+" + "-" * 50)

    # Add task rows
    for task in tasks:
        lines.append(format_task_row(task))

    return "\n".join(lines)


def show_empty_message() -> str:
    """Get empty state message.

    Returns:
        Friendly message when no tasks exist
    """
    return "No tasks yet. Add your first task to get started!"


def show_success(message: str) -> str:
    """Format success message.

    Args:
        message: Success message text

    Returns:
        Formatted success message
    """
    return f"✓ {message}"


def show_error(message: str) -> str:
    """Format error message.

    Args:
        message: Error message text

    Returns:
        Formatted error message
    """
    return f"Error: {message}"
