"""Unit tests for TaskManager business logic."""

import unittest
from src.task_manager import TaskManager
from src.models import Task, TaskStatus


class TestTaskManagerInit(unittest.TestCase):
    """Test TaskManager initialization."""

    def test_init_empty_tasks(self):
        """TaskManager should initialize with empty task list."""
        manager = TaskManager()
        self.assertEqual(len(manager.get_all_tasks()), 0)

    def test_init_next_id_starts_at_one(self):
        """TaskManager should start ID counter at 1."""
        manager = TaskManager()
        task = manager.add_task("First Task")
        self.assertEqual(task.id, 1)


class TestTaskManagerAddTask(unittest.TestCase):
    """Test TaskManager.add_task method."""

    def setUp(self):
        """Create fresh TaskManager for each test."""
        self.manager = TaskManager()

    def test_add_task_with_title_only(self):
        """Should create task with title and default values."""
        task = self.manager.add_task("Buy groceries")
        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(task.description, "")
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertEqual(task.id, 1)

    def test_add_task_with_title_and_description(self):
        """Should create task with both title and description."""
        task = self.manager.add_task("Buy groceries", "Milk, eggs, bread")
        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(task.description, "Milk, eggs, bread")
        self.assertEqual(task.status, TaskStatus.PENDING)

    def test_add_task_increments_id(self):
        """Each new task should get incremented ID."""
        task1 = self.manager.add_task("Task 1")
        task2 = self.manager.add_task("Task 2")
        task3 = self.manager.add_task("Task 3")
        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)
        self.assertEqual(task3.id, 3)

    def test_add_task_adds_to_list(self):
        """Adding task should increase task count."""
        self.assertEqual(len(self.manager.get_all_tasks()), 0)
        self.manager.add_task("Task 1")
        self.assertEqual(len(self.manager.get_all_tasks()), 1)
        self.manager.add_task("Task 2")
        self.assertEqual(len(self.manager.get_all_tasks()), 2)

    def test_add_task_with_empty_title_raises_error(self):
        """Empty title should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            self.manager.add_task("")
        self.assertEqual(str(context.exception), "Title cannot be empty")

    def test_add_task_with_whitespace_title_raises_error(self):
        """Whitespace-only title should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            self.manager.add_task("   ")
        self.assertEqual(str(context.exception), "Title cannot be empty")

    def test_add_task_strips_whitespace(self):
        """Title should be stripped of leading/trailing whitespace."""
        task = self.manager.add_task("  Task with spaces  ")
        self.assertEqual(task.title, "Task with spaces")


class TestTaskManagerGetAllTasks(unittest.TestCase):
    """Test TaskManager.get_all_tasks method."""

    def setUp(self):
        """Create fresh TaskManager with sample tasks."""
        self.manager = TaskManager()
        self.task1 = self.manager.add_task("Task 1", "Description 1")
        self.task2 = self.manager.add_task("Task 2", "Description 2")

    def test_get_all_tasks_returns_list(self):
        """Should return a list."""
        tasks = self.manager.get_all_tasks()
        self.assertIsInstance(tasks, list)

    def test_get_all_tasks_returns_all(self):
        """Should return all tasks."""
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 2)

    def test_get_all_tasks_returns_correct_tasks(self):
        """Should return the correct task objects."""
        tasks = self.manager.get_all_tasks()
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[0].title, "Task 1")
        self.assertEqual(tasks[1].id, 2)
        self.assertEqual(tasks[1].title, "Task 2")

    def test_get_all_tasks_returns_copy(self):
        """Should return a copy, not the internal list."""
        tasks1 = self.manager.get_all_tasks()
        tasks2 = self.manager.get_all_tasks()
        self.assertIsNot(tasks1, tasks2)

    def test_get_all_tasks_when_empty(self):
        """Should return empty list when no tasks exist."""
        manager = TaskManager()
        tasks = manager.get_all_tasks()
        self.assertEqual(tasks, [])


class TestTaskManagerGetTaskById(unittest.TestCase):
    """Test TaskManager.get_task_by_id method."""

    def setUp(self):
        """Create fresh TaskManager with sample tasks."""
        self.manager = TaskManager()
        self.task1 = self.manager.add_task("Task 1")
        self.task2 = self.manager.add_task("Task 2")

    def test_get_task_by_id_found(self):
        """Should return task when ID exists."""
        task = self.manager.get_task_by_id(1)
        self.assertIsNotNone(task)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Task 1")

    def test_get_task_by_id_not_found(self):
        """Should return None when ID doesn't exist."""
        task = self.manager.get_task_by_id(999)
        self.assertIsNone(task)

    def test_get_task_by_id_returns_same_object(self):
        """Should return reference to the same task object."""
        task1 = self.manager.get_task_by_id(1)
        task2 = self.manager.get_task_by_id(1)
        self.assertIs(task1, task2)


class TestTaskManagerUpdateTask(unittest.TestCase):
    """Test TaskManager.update_task method."""

    def setUp(self):
        """Create fresh TaskManager with sample task."""
        self.manager = TaskManager()
        self.task = self.manager.add_task("Original Title", "Original Description")

    def test_update_task_title_only(self):
        """Should update title while keeping description."""
        updated = self.manager.update_task(1, title="New Title")
        self.assertEqual(updated.title, "New Title")
        self.assertEqual(updated.description, "Original Description")

    def test_update_task_description_only(self):
        """Should update description while keeping title."""
        updated = self.manager.update_task(1, description="New Description")
        self.assertEqual(updated.title, "Original Title")
        self.assertEqual(updated.description, "New Description")

    def test_update_task_both_fields(self):
        """Should update both title and description."""
        updated = self.manager.update_task(1, title="New Title", description="New Description")
        self.assertEqual(updated.title, "New Title")
        self.assertEqual(updated.description, "New Description")

    def test_update_task_with_empty_title_raises_error(self):
        """Empty title should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            self.manager.update_task(1, title="")
        self.assertEqual(str(context.exception), "Title cannot be empty")

    def test_update_task_not_found_raises_error(self):
        """Non-existent task ID should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            self.manager.update_task(999, title="New Title")
        self.assertEqual(str(context.exception), "Task with ID 999 not found")

    def test_update_task_strips_whitespace(self):
        """Title should be stripped of whitespace."""
        updated = self.manager.update_task(1, title="  New Title  ")
        self.assertEqual(updated.title, "New Title")

    def test_update_task_returns_same_object(self):
        """Should return reference to the same task object."""
        updated = self.manager.update_task(1, title="New Title")
        original = self.manager.get_task_by_id(1)
        self.assertIs(updated, original)


class TestTaskManagerDeleteTask(unittest.TestCase):
    """Test TaskManager.delete_task method."""

    def setUp(self):
        """Create fresh TaskManager with sample tasks."""
        self.manager = TaskManager()
        self.task1 = self.manager.add_task("Task 1")
        self.task2 = self.manager.add_task("Task 2")
        self.task3 = self.manager.add_task("Task 3")

    def test_delete_task_removes_from_list(self):
        """Should remove task from list."""
        self.assertEqual(len(self.manager.get_all_tasks()), 3)
        self.manager.delete_task(2)
        self.assertEqual(len(self.manager.get_all_tasks()), 2)

    def test_delete_task_returns_true(self):
        """Should return True on successful deletion."""
        result = self.manager.delete_task(1)
        self.assertTrue(result)

    def test_delete_task_not_found_raises_error(self):
        """Non-existent task ID should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            self.manager.delete_task(999)
        self.assertEqual(str(context.exception), "Task with ID 999 not found")

    def test_delete_task_id_not_reused(self):
        """Deleted task ID should not be reused."""
        self.manager.delete_task(2)
        new_task = self.manager.add_task("New Task")
        self.assertEqual(new_task.id, 4)  # Next ID is 4, not 2

    def test_delete_task_correct_task_removed(self):
        """Should remove the correct task."""
        self.manager.delete_task(2)
        tasks = self.manager.get_all_tasks()
        task_ids = [t.id for t in tasks]
        self.assertIn(1, task_ids)
        self.assertNotIn(2, task_ids)
        self.assertIn(3, task_ids)


class TestTaskManagerToggleStatus(unittest.TestCase):
    """Test TaskManager.toggle_status method."""

    def setUp(self):
        """Create fresh TaskManager with sample task."""
        self.manager = TaskManager()
        self.task = self.manager.add_task("Test Task")

    def test_toggle_status_pending_to_completed(self):
        """Should toggle PENDING to COMPLETED."""
        self.assertEqual(self.task.status, TaskStatus.PENDING)
        updated = self.manager.toggle_status(1)
        self.assertEqual(updated.status, TaskStatus.COMPLETED)

    def test_toggle_status_completed_to_pending(self):
        """Should toggle COMPLETED back to PENDING."""
        self.manager.toggle_status(1)  # PENDING -> COMPLETED
        updated = self.manager.toggle_status(1)  # COMPLETED -> PENDING
        self.assertEqual(updated.status, TaskStatus.PENDING)

    def test_toggle_status_not_found_raises_error(self):
        """Non-existent task ID should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            self.manager.toggle_status(999)
        self.assertEqual(str(context.exception), "Task with ID 999 not found")

    def test_toggle_status_returns_same_object(self):
        """Should return reference to the same task object."""
        updated = self.manager.toggle_status(1)
        original = self.manager.get_task_by_id(1)
        self.assertIs(updated, original)


if __name__ == "__main__":
    unittest.main()
