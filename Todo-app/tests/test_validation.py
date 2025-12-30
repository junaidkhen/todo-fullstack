"""Unit tests for input validation."""

import unittest
from src.validation import validate_title, validate_task_id
from src.models import Task, TaskStatus


class TestValidateTitle(unittest.TestCase):
    """Test validate_title function."""

    def test_valid_title(self):
        """Valid title should be returned as-is after strip."""
        result = validate_title("Buy groceries")
        self.assertEqual(result, "Buy groceries")

    def test_title_with_leading_whitespace(self):
        """Title with leading whitespace should be stripped."""
        result = validate_title("  Task with spaces")
        self.assertEqual(result, "Task with spaces")

    def test_title_with_trailing_whitespace(self):
        """Title with trailing whitespace should be stripped."""
        result = validate_title("Task with spaces  ")
        self.assertEqual(result, "Task with spaces")

    def test_title_with_both_whitespace(self):
        """Title with both leading and trailing whitespace should be stripped."""
        result = validate_title("  Task  ")
        self.assertEqual(result, "Task")

    def test_empty_string_raises_error(self):
        """Empty string should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            validate_title("")
        self.assertEqual(str(context.exception), "Title cannot be empty")

    def test_whitespace_only_raises_error(self):
        """Whitespace-only string should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            validate_title("   ")
        self.assertEqual(str(context.exception), "Title cannot be empty")

    def test_tabs_and_newlines_raises_error(self):
        """String with only tabs and newlines should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            validate_title("\t\n  ")
        self.assertEqual(str(context.exception), "Title cannot be empty")


class TestValidateTaskId(unittest.TestCase):
    """Test validate_task_id function."""

    def setUp(self):
        """Create sample tasks for testing."""
        self.tasks = [
            Task(id=1, title="Task 1"),
            Task(id=2, title="Task 2"),
            Task(id=5, title="Task 5"),
        ]

    def test_valid_id_as_string(self):
        """Valid ID string should be converted to integer."""
        result = validate_task_id("1", self.tasks)
        self.assertEqual(result, 1)
        self.assertIsInstance(result, int)

    def test_valid_id_with_whitespace(self):
        """Valid ID with whitespace should be stripped and converted."""
        result = validate_task_id("  2  ", self.tasks)
        self.assertEqual(result, 2)

    def test_non_numeric_raises_error(self):
        """Non-numeric ID should raise ValueError with descriptive message."""
        with self.assertRaises(ValueError) as context:
            validate_task_id("abc", self.tasks)
        self.assertEqual(str(context.exception), "Invalid task ID format: 'abc'")

    def test_negative_number_raises_error(self):
        """Negative number should raise ValueError (not in task list)."""
        with self.assertRaises(ValueError) as context:
            validate_task_id("-1", self.tasks)
        self.assertEqual(str(context.exception), "Invalid task ID format: '-1'")

    def test_float_raises_error(self):
        """Float number should raise ValueError (not an integer)."""
        with self.assertRaises(ValueError) as context:
            validate_task_id("1.5", self.tasks)
        self.assertEqual(str(context.exception), "Invalid task ID format: '1.5'")

    def test_non_existent_id_raises_error(self):
        """ID not in task list should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            validate_task_id("999", self.tasks)
        self.assertEqual(str(context.exception), "Task with ID 999 not found")

    def test_empty_string_raises_error(self):
        """Empty string should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            validate_task_id("", self.tasks)
        self.assertEqual(str(context.exception), "Invalid task ID format: ''")

    def test_gap_in_ids(self):
        """Should handle tasks with non-sequential IDs."""
        result = validate_task_id("5", self.tasks)
        self.assertEqual(result, 5)


if __name__ == "__main__":
    unittest.main()
