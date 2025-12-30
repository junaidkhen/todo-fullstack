"""Task management business logic."""

from src.models import Task, TaskStatus
from src.validation import validate_title


class TaskManager:
    """Manages the collection of tasks and enforces business rules.

    Attributes:
        _tasks: In-memory list of all active tasks
        _next_id: Counter for generating unique task IDs
    """

    def __init__(self) -> None:
        """Initialize empty task manager."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Create and add a new task.

        Args:
            title: Task title (required, non-empty)
            description: Task description (optional)

        Returns:
            The newly created Task object

        Raises:
            ValueError: If title is empty or whitespace-only
        """
        # Validate title
        validated_title = validate_title(title)

        # Create new task
        task = Task(
            id=self._next_id,
            title=validated_title,
            description=description,
            status=TaskStatus.PENDING,
        )

        # Add to list and increment ID counter
        self._tasks.append(task)
        self._next_id += 1

        return task

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks.

        Returns:
            List of all tasks (empty list if no tasks exist)
        """
        return self._tasks.copy()

    def get_task_by_id(self, task_id: int) -> Task | None:
        """Find task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task object if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(
        self, task_id: int, title: str | None = None, description: str | None = None
    ) -> Task:
        """Update existing task.

        Args:
            task_id: ID of task to update
            title: New title (optional, validates if provided)
            description: New description (optional)

        Returns:
            Updated Task object

        Raises:
            ValueError: If task not found or title is empty
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found")

        # Update title if provided
        if title is not None:
            validated_title = validate_title(title)
            task.title = validated_title

        # Update description if provided
        if description is not None:
            task.description = description

        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID.

        Args:
            task_id: ID of task to delete

        Returns:
            True if task was deleted

        Raises:
            ValueError: If task not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found")

        self._tasks.remove(task)
        # Note: _next_id is NOT decremented (IDs never reused)
        return True

    def toggle_status(self, task_id: int) -> Task:
        """Toggle task completion status.

        Args:
            task_id: ID of task to toggle

        Returns:
            Updated Task object with new status

        Raises:
            ValueError: If task not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found")

        # Toggle status
        if task.status == TaskStatus.PENDING:
            task.status = TaskStatus.COMPLETED
        else:
            task.status = TaskStatus.PENDING

        return task
