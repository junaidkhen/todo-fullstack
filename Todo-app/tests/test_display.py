"""Unit tests for display formatting."""

import unittest
from src.display import (
    truncate,
    format_task_row,
    format_task_table,
    show_empty_message,
    show_success,
    show_error,
)
from src.models import Task, TaskStatus


class TestTruncate(unittest.TestCase):
    """Test truncate function."""

    def test_text_shorter_than_max(self):
        """Text shorter than max length should be returned as-is."""
        result = truncate("Short text", 50)
        self.assertEqual(result, "Short text")

    def test_text_equal_to_max(self):
        """Text equal to max length should be returned as-is."""
        result = truncate("X" * 50, 50)
        self.assertEqual(result, "X" * 50)

    def test_text_longer_than_max(self):
        """Text longer than max should be truncated with ellipsis."""
        result = truncate("This is a very long text that needs truncation", 20)
        self.assertEqual(result, "This is a very lo...")
        self.assertEqual(len(result), 20)

    def test_truncate_default_max_length(self):
        """Default max length should be 50."""
        long_text = "X" * 60
        result = truncate(long_text)
        self.assertEqual(len(result), 50)
        self.assertTrue(result.endswith("..."))

    def test_truncate_preserves_ellipsis_length(self):
        """Truncated text should always be exactly max_length."""
        result = truncate("Very long text here", 10)
        self.assertEqual(len(result), 10)
        self.assertEqual(result, "Very lo...")


class TestFormatTaskRow(unittest.TestCase):
    """Test format_task_row function."""

    def test_format_pending_task_with_description(self):
        """Pending task with description should format correctly."""
        task = Task(id=1, title="Buy groceries", description="Milk and eggs", status=TaskStatus.PENDING)
        result = format_task_row(task)
        self.assertIn("  1", result)  # ID right-aligned
        self.assertIn("Buy groceries", result)
        self.assertIn("[ ] Pend.", result)
        self.assertIn("Milk and eggs", result)

    def test_format_completed_task(self):
        """Completed task should show checkmark."""
        task = Task(id=2, title="Finish report", status=TaskStatus.COMPLETED)
        result = format_task_row(task)
        self.assertIn("[✓] Comp.", result)

    def test_format_task_without_description(self):
        """Task without description should show empty description field."""
        task = Task(id=3, title="Simple task", description="")
        result = format_task_row(task)
        self.assertIn("Simple task", result)
        # Description field should be empty (not "None" or similar)
        self.assertNotIn("None", result)

    def test_format_task_truncates_long_title(self):
        """Long title should be truncated to 25 characters."""
        long_title = "This is a very long task title that needs truncation"
        task = Task(id=4, title=long_title)
        result = format_task_row(task)
        self.assertIn("...", result)
        # Title field should be truncated
        self.assertNotIn(long_title, result)

    def test_format_task_truncates_long_description(self):
        """Long description should be truncated to 50 characters."""
        long_desc = "This is a very long description that definitely needs to be truncated for display"
        task = Task(id=5, title="Task", description=long_desc)
        result = format_task_row(task)
        self.assertIn("...", result)

    def test_format_task_has_pipe_separators(self):
        """Row should have pipe separators."""
        task = Task(id=1, title="Test")
        result = format_task_row(task)
        self.assertIn("|", result)
        # Should have 3 separators (4 columns)
        self.assertEqual(result.count("|"), 3)

    def test_format_task_double_digit_id(self):
        """Double-digit IDs should format correctly."""
        task = Task(id=42, title="Test")
        result = format_task_row(task)
        self.assertIn(" 42", result)

    def test_format_task_triple_digit_id(self):
        """Triple-digit IDs should format correctly."""
        task = Task(id=999, title="Test")
        result = format_task_row(task)
        self.assertIn("999", result)


class TestFormatTaskTable(unittest.TestCase):
    """Test format_task_table function."""

    def test_format_empty_table(self):
        """Empty task list should still show header."""
        result = format_task_table([])
        self.assertIn("ID", result)
        self.assertIn("Title", result)
        self.assertIn("Status", result)
        self.assertIn("Description", result)
        # Should have header and separator, but no data rows
        lines = result.split("\n")
        self.assertEqual(len(lines), 2)

    def test_format_table_with_single_task(self):
        """Table with one task should have 3 lines."""
        task = Task(id=1, title="Test Task")
        result = format_task_table([task])
        lines = result.split("\n")
        self.assertEqual(len(lines), 3)  # header + separator + 1 row

    def test_format_table_with_multiple_tasks(self):
        """Table with multiple tasks should have correct number of lines."""
        tasks = [
            Task(id=1, title="Task 1"),
            Task(id=2, title="Task 2"),
            Task(id=3, title="Task 3"),
        ]
        result = format_task_table(tasks)
        lines = result.split("\n")
        self.assertEqual(len(lines), 5)  # header + separator + 3 rows

    def test_format_table_has_header(self):
        """Table should have proper header."""
        tasks = [Task(id=1, title="Test")]
        result = format_task_table(tasks)
        lines = result.split("\n")
        self.assertIn("ID", lines[0])
        self.assertIn("Title", lines[0])
        self.assertIn("Status", lines[0])
        self.assertIn("Description", lines[0])

    def test_format_table_has_separator(self):
        """Table should have separator line with dashes."""
        tasks = [Task(id=1, title="Test")]
        result = format_task_table(tasks)
        lines = result.split("\n")
        self.assertIn("---", lines[1])
        self.assertIn("+", lines[1])

    def test_format_table_preserves_task_order(self):
        """Tasks should appear in the same order."""
        tasks = [
            Task(id=1, title="First"),
            Task(id=2, title="Second"),
            Task(id=3, title="Third"),
        ]
        result = format_task_table(tasks)
        # First should appear before Second
        first_pos = result.find("First")
        second_pos = result.find("Second")
        third_pos = result.find("Third")
        self.assertLess(first_pos, second_pos)
        self.assertLess(second_pos, third_pos)


class TestShowEmptyMessage(unittest.TestCase):
    """Test show_empty_message function."""

    def test_returns_string(self):
        """Should return a string."""
        result = show_empty_message()
        self.assertIsInstance(result, str)

    def test_message_is_friendly(self):
        """Message should be friendly and helpful."""
        result = show_empty_message()
        self.assertTrue(len(result) > 0)
        # Should mention tasks or getting started
        self.assertTrue("task" in result.lower() or "start" in result.lower())


class TestShowSuccess(unittest.TestCase):
    """Test show_success function."""

    def test_formats_with_checkmark(self):
        """Success message should include checkmark."""
        result = show_success("Operation completed")
        self.assertIn("✓", result)
        self.assertIn("Operation completed", result)

    def test_preserves_message(self):
        """Should preserve the original message."""
        msg = "Task added successfully"
        result = show_success(msg)
        self.assertIn(msg, result)


class TestShowError(unittest.TestCase):
    """Test show_error function."""

    def test_formats_with_error_prefix(self):
        """Error message should include 'Error:' prefix."""
        result = show_error("Something went wrong")
        self.assertIn("Error:", result)
        self.assertIn("Something went wrong", result)

    def test_preserves_message(self):
        """Should preserve the original error message."""
        msg = "Invalid input"
        result = show_error(msg)
        self.assertIn(msg, result)


if __name__ == "__main__":
    unittest.main()
