"""Unit tests for data models."""

import unittest
from src.models import Task, TaskStatus


class TestTaskStatus(unittest.TestCase):
    """Test TaskStatus enum."""

    def test_pending_value(self):
        """TaskStatus.PENDING should have value 'Pending'."""
        self.assertEqual(TaskStatus.PENDING.value, "Pending")

    def test_completed_value(self):
        """TaskStatus.COMPLETED should have value 'Completed'."""
        self.assertEqual(TaskStatus.COMPLETED.value, "Completed")

    def test_enum_members(self):
        """TaskStatus should have exactly 2 members."""
        self.assertEqual(len(TaskStatus), 2)


class TestTask(unittest.TestCase):
    """Test Task dataclass."""

    def test_task_creation_with_all_fields(self):
        """Task should be created with all fields provided."""
        task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            status=TaskStatus.PENDING,
        )
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.status, TaskStatus.PENDING)

    def test_task_creation_with_minimal_fields(self):
        """Task should use default values for optional fields."""
        task = Task(id=2, title="Minimal Task")
        self.assertEqual(task.id, 2)
        self.assertEqual(task.title, "Minimal Task")
        self.assertEqual(task.description, "")
        self.assertEqual(task.status, TaskStatus.PENDING)

    def test_task_creation_with_completed_status(self):
        """Task should allow COMPLETED status."""
        task = Task(id=3, title="Done Task", status=TaskStatus.COMPLETED)
        self.assertEqual(task.status, TaskStatus.COMPLETED)

    def test_task_immutability_not_enforced(self):
        """Task fields should be mutable (dataclass default behavior)."""
        task = Task(id=4, title="Original")
        task.title = "Modified"
        self.assertEqual(task.title, "Modified")


if __name__ == "__main__":
    unittest.main()
