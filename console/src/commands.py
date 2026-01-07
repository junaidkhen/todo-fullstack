"""Command handlers for Todo application."""

import sys
from task_manager import TaskManager
from validation import validate_task_id
from display import (
    format_task_table,
    show_empty_message,
    show_success,
    show_error,
)


def handle_add(manager: TaskManager) -> None:
    """Handle the 'add' command to create a new task.

    Prompts user for title and description, then adds task to manager.

    Args:
        manager: TaskManager instance to add task to
    """
    try:
        title = input("Enter task title: ")
        description = input("Enter task description (optional): ").strip()

        # add_task will validate the title
        task = manager.add_task(title, description)
        print(show_success(f"Task #{task.id} added: {task.title}"))

    except ValueError as e:
        print(show_error(str(e)))


def handle_list(manager: TaskManager) -> None:
    """Handle the 'list' command to display all tasks.

    Shows empty message if no tasks exist, otherwise displays formatted table.

    Args:
        manager: TaskManager instance to get tasks from
    """
    tasks = manager.get_all_tasks()

    if not tasks:
        print(show_empty_message())
    else:
        print(format_task_table(tasks))


def handle_mark(manager: TaskManager) -> None:
    """Handle the 'mark' command to toggle task completion status.

    Prompts user for task ID, validates it, toggles status, and shows feedback.

    Args:
        manager: TaskManager instance to mark task in
    """
    try:
        task_id_str = input("Enter task ID to mark: ")

        # Validate task ID
        task_id = validate_task_id(task_id_str, manager.get_all_tasks())

        # Toggle the status
        task = manager.toggle_status(task_id)

        # Show success message with new status
        status_word = "completed" if task.status.value == "Completed" else "pending"
        print(show_success(f"Task #{task.id} '{task.title}' marked as {status_word}"))

    except ValueError as e:
        print(show_error(str(e)))


def handle_update(manager: TaskManager) -> None:
    """Handle the 'update' command to modify task details.

    Prompts user for task ID, new title (optional), and new description (optional).
    At least one field must be updated. Empty strings preserve current values.

    Args:
        manager: TaskManager instance to update task in
    """
    try:
        task_id_str = input("Enter task ID to update: ")

        # Validate task ID
        task_id = validate_task_id(task_id_str, manager.get_all_tasks())

        # Get new values (don't strip yet - let user input empty strings)
        new_title = input("Enter new title (leave empty to keep current): ")
        new_description = input("Enter new description (leave empty to keep current): ")

        # Strip for emptiness check, but preserve original for processing
        new_title_stripped = new_title.strip()
        new_description_stripped = new_description.strip()

        # Determine what to update: if user entered something (even whitespace), we'll try to update it
        # This allows validation errors to be caught properly
        title_param = new_title_stripped if new_title else None
        description_param = new_description_stripped if new_description else None

        # Check if at least one field is being updated
        if title_param is None and description_param is None:
            print(show_error("No changes provided. Please enter a new title or description."))
            return

        # Update the task (this will validate title if provided)
        task = manager.update_task(task_id, title=title_param, description=description_param)

        # Show success message
        print(show_success(f"Task #{task.id} updated successfully"))

    except ValueError as e:
        print(show_error(str(e)))


def handle_delete(manager: TaskManager) -> None:
    """Handle the 'delete' command to permanently remove a task.

    Prompts user for task ID, validates it, deletes the task, and shows confirmation.

    Args:
        manager: TaskManager instance to delete task from
    """
    try:
        task_id_str = input("Enter task ID to delete: ")

        # Validate task ID
        task_id = validate_task_id(task_id_str, manager.get_all_tasks())

        # Get task details before deletion for feedback
        task = manager.get_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found")

        task_title = task.title

        # Delete the task
        manager.delete_task(task_id)

        # Show success message
        print(show_success(f"Task #{task_id} '{task_title}' deleted successfully"))

    except ValueError as e:
        print(show_error(str(e)))


def handle_help() -> None:
    """Display available commands and usage information."""
    help_text = """
Available Commands:
  add     - Add a new task
  list    - View all tasks
  mark    - Mark a task as complete/incomplete
  update  - Update a task's title or description
  delete  - Delete a task
  help    - Show this help message
  exit    - Exit the application (or use 'quit')

Usage:
  Simply type the command name at the prompt.
  The application will guide you through any additional inputs needed.
"""
    print(help_text)
