"""Integration tests for command workflows."""

import unittest
from unittest.mock import patch
from io import StringIO
from src.task_manager import TaskManager
from src.commands import handle_add, handle_list, handle_help, handle_mark


class TestHandleAdd(unittest.TestCase):
    """Test handle_add command integration."""

    def setUp(self):
        """Create fresh TaskManager for each test."""
        self.manager = TaskManager()

    @patch("builtins.input", side_effect=["Buy groceries", "Milk and eggs"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_add_task_with_description(self, mock_stdout, mock_input):
        """Should prompt for title and description, then add task."""
        handle_add(self.manager)

        output = mock_stdout.getvalue()
        # Should show success message
        self.assertIn("✓", output)
        self.assertIn("added", output.lower())

        # Task should be in manager
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Buy groceries")
        self.assertEqual(tasks[0].description, "Milk and eggs")

    @patch("builtins.input", side_effect=["Simple task", ""])
    @patch("sys.stdout", new_callable=StringIO)
    def test_add_task_without_description(self, mock_stdout, mock_input):
        """Should allow empty description."""
        handle_add(self.manager)

        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Simple task")
        self.assertEqual(tasks[0].description, "")

    @patch("builtins.input", side_effect=["   ", "Valid task", "Description"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_add_task_with_empty_title_shows_error(self, mock_stdout, mock_input):
        """Should reject empty title and show error."""
        handle_add(self.manager)

        output = mock_stdout.getvalue()
        # Should show error for empty title
        self.assertIn("Error:", output)
        self.assertIn("empty", output.lower())

    @patch("builtins.input", side_effect=["  Task with spaces  ", "  Desc with spaces  "])
    @patch("sys.stdout", new_callable=StringIO)
    def test_add_task_strips_whitespace(self, mock_stdout, mock_input):
        """Should strip whitespace from inputs."""
        handle_add(self.manager)

        tasks = self.manager.get_all_tasks()
        self.assertEqual(tasks[0].title, "Task with spaces")
        self.assertEqual(tasks[0].description, "Desc with spaces")

    @patch("builtins.input", side_effect=["First", "A", "Second", "B", "Third", "C"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_add_multiple_tasks(self, mock_stdout, mock_input):
        """Should be able to add multiple tasks."""
        handle_add(self.manager)
        handle_add(self.manager)
        handle_add(self.manager)

        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[1].id, 2)
        self.assertEqual(tasks[2].id, 3)


class TestHandleList(unittest.TestCase):
    """Test handle_list command integration."""

    def setUp(self):
        """Create fresh TaskManager for each test."""
        self.manager = TaskManager()

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_empty_tasks(self, mock_stdout):
        """Should show empty message when no tasks exist."""
        handle_list(self.manager)

        output = mock_stdout.getvalue()
        self.assertIn("No tasks", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_single_task(self, mock_stdout):
        """Should display single task in table format."""
        self.manager.add_task("Buy groceries", "Milk and eggs")
        handle_list(self.manager)

        output = mock_stdout.getvalue()
        # Should show table header
        self.assertIn("ID", output)
        self.assertIn("Title", output)
        self.assertIn("Status", output)
        self.assertIn("Description", output)
        # Should show task data
        self.assertIn("Buy groceries", output)
        self.assertIn("Milk and eggs", output)
        self.assertIn("[ ] Pend.", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_multiple_tasks(self, mock_stdout):
        """Should display all tasks in table format."""
        self.manager.add_task("Task 1", "Description 1")
        self.manager.add_task("Task 2", "Description 2")
        self.manager.add_task("Task 3", "Description 3")
        handle_list(self.manager)

        output = mock_stdout.getvalue()
        self.assertIn("Task 1", output)
        self.assertIn("Task 2", output)
        self.assertIn("Task 3", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_shows_completed_tasks(self, mock_stdout):
        """Should show completed status for completed tasks."""
        task = self.manager.add_task("Completed task")
        self.manager.toggle_status(task.id)
        handle_list(self.manager)

        output = mock_stdout.getvalue()
        self.assertIn("[✓] Comp.", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_preserves_task_order(self, mock_stdout):
        """Should display tasks in order they were added."""
        self.manager.add_task("First")
        self.manager.add_task("Second")
        self.manager.add_task("Third")
        handle_list(self.manager)

        output = mock_stdout.getvalue()
        # First should appear before Second
        first_pos = output.find("First")
        second_pos = output.find("Second")
        third_pos = output.find("Third")
        self.assertLess(first_pos, second_pos)
        self.assertLess(second_pos, third_pos)


class TestHandleHelp(unittest.TestCase):
    """Test handle_help command integration."""

    @patch("sys.stdout", new_callable=StringIO)
    def test_help_shows_available_commands(self, mock_stdout):
        """Should display list of available commands."""
        handle_help()

        output = mock_stdout.getvalue()
        # Should mention key commands
        self.assertIn("add", output.lower())
        self.assertIn("list", output.lower())
        self.assertIn("help", output.lower())
        self.assertIn("exit", output.lower() or "quit", output.lower())

    @patch("sys.stdout", new_callable=StringIO)
    def test_help_is_readable(self, mock_stdout):
        """Help output should be non-empty and formatted."""
        handle_help()

        output = mock_stdout.getvalue()
        self.assertTrue(len(output) > 0)
        # Should have some structure (newlines for readability)
        self.assertIn("\n", output)


class TestHandleMark(unittest.TestCase):
    """Test handle_mark command integration."""

    def setUp(self):
        """Create fresh TaskManager with sample tasks."""
        self.manager = TaskManager()
        self.task1 = self.manager.add_task("Task 1")
        self.task2 = self.manager.add_task("Task 2")
        self.task3 = self.manager.add_task("Task 3")

    @patch("builtins.input", return_value="1")
    @patch("sys.stdout", new_callable=StringIO)
    def test_mark_pending_task_as_completed(self, mock_stdout, mock_input):
        """Should mark pending task as completed."""
        handle_mark(self.manager)

        output = mock_stdout.getvalue()
        # Should show success message
        self.assertIn("✓", output)
        self.assertIn("completed", output.lower())

        # Task should be marked as completed
        task = self.manager.get_task_by_id(1)
        self.assertEqual(task.status.value, "Completed")

    @patch("builtins.input", return_value="1")
    @patch("sys.stdout", new_callable=StringIO)
    def test_mark_completed_task_as_pending(self, mock_stdout, mock_input):
        """Should toggle completed task back to pending."""
        # First mark as completed
        self.manager.toggle_status(1)

        # Then toggle back to pending
        handle_mark(self.manager)

        output = mock_stdout.getvalue()
        self.assertIn("✓", output)
        self.assertIn("pending", output.lower())

        # Task should be marked as pending
        task = self.manager.get_task_by_id(1)
        self.assertEqual(task.status.value, "Pending")

    @patch("builtins.input", return_value="999")
    @patch("sys.stdout", new_callable=StringIO)
    def test_mark_nonexistent_task_shows_error(self, mock_stdout, mock_input):
        """Should show error for non-existent task ID."""
        handle_mark(self.manager)

        output = mock_stdout.getvalue()
        self.assertIn("Error:", output)
        self.assertIn("999", output)

    @patch("builtins.input", return_value="abc")
    @patch("sys.stdout", new_callable=StringIO)
    def test_mark_invalid_id_format_shows_error(self, mock_stdout, mock_input):
        """Should show error for invalid ID format."""
        handle_mark(self.manager)

        output = mock_stdout.getvalue()
        self.assertIn("Error:", output)
        output_lower = output.lower()
        self.assertTrue("invalid" in output_lower or "format" in output_lower)

    @patch("builtins.input", return_value="2")
    @patch("sys.stdout", new_callable=StringIO)
    def test_mark_shows_task_title_in_feedback(self, mock_stdout, mock_input):
        """Should show task title in success message."""
        handle_mark(self.manager)

        output = mock_stdout.getvalue()
        self.assertIn("Task 2", output)

    @patch("builtins.input", side_effect=["1", "2", "3"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_mark_multiple_tasks(self, mock_stdout, mock_input):
        """Should be able to mark multiple tasks."""
        handle_mark(self.manager)
        handle_mark(self.manager)
        handle_mark(self.manager)

        # All three tasks should be completed
        self.assertEqual(self.manager.get_task_by_id(1).status.value, "Completed")
        self.assertEqual(self.manager.get_task_by_id(2).status.value, "Completed")
        self.assertEqual(self.manager.get_task_by_id(3).status.value, "Completed")


class TestHandleDelete(unittest.TestCase):
    """Test handle_delete command integration."""

    def setUp(self):
        """Create fresh TaskManager with sample tasks."""
        self.manager = TaskManager()
        self.task1 = self.manager.add_task("Task 1", "Description 1")
        self.task2 = self.manager.add_task("Task 2", "Description 2")
        self.task3 = self.manager.add_task("Task 3", "Description 3")

    @patch("builtins.input", return_value="1")
    @patch("sys.stdout", new_callable=StringIO)
    def test_delete_existing_task(self, mock_stdout, mock_input):
        """Should delete task and show success message."""
        from src.commands import handle_delete
        handle_delete(self.manager)

        output = mock_stdout.getvalue()
        # Should show success message
        self.assertIn("✓", output)
        self.assertIn("deleted", output.lower())

        # Task should be deleted
        self.assertEqual(len(self.manager.get_all_tasks()), 2)
        self.assertIsNone(self.manager.get_task_by_id(1))

    @patch("builtins.input", return_value="999")
    @patch("sys.stdout", new_callable=StringIO)
    def test_delete_nonexistent_task_shows_error(self, mock_stdout, mock_input):
        """Should show error for non-existent task ID."""
        from src.commands import handle_delete
        handle_delete(self.manager)

        output = mock_stdout.getvalue()
        self.assertIn("Error:", output)
        self.assertIn("999", output)

        # No tasks should be deleted
        self.assertEqual(len(self.manager.get_all_tasks()), 3)

    @patch("builtins.input", return_value="abc")
    @patch("sys.stdout", new_callable=StringIO)
    def test_delete_invalid_id_format_shows_error(self, mock_stdout, mock_input):
        """Should show error for invalid ID format."""
        from src.commands import handle_delete
        handle_delete(self.manager)

        output = mock_stdout.getvalue()
        self.assertIn("Error:", output)
        output_lower = output.lower()
        self.assertTrue("invalid" in output_lower or "format" in output_lower)

    @patch("builtins.input", return_value="2")
    @patch("sys.stdout", new_callable=StringIO)
    def test_delete_shows_task_title_in_feedback(self, mock_stdout, mock_input):
        """Should show task title in success message."""
        from src.commands import handle_delete
        handle_delete(self.manager)

        output = mock_stdout.getvalue()
        # Should mention the task ID in feedback
        self.assertIn("#2", output)

    @patch("builtins.input", side_effect=["1", "3"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_delete_multiple_tasks(self, mock_stdout, mock_input):
        """Should be able to delete multiple tasks."""
        from src.commands import handle_delete
        handle_delete(self.manager)
        handle_delete(self.manager)

        # Only task 2 should remain
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, 2)

    @patch("builtins.input", side_effect=["2"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_delete_preserves_other_task_ids(self, mock_stdout, mock_input):
        """Deleting a task should not affect other task IDs."""
        from src.commands import handle_delete
        handle_delete(self.manager)

        tasks = self.manager.get_all_tasks()
        # Task 1 and 3 should still exist with original IDs
        task_ids = [t.id for t in tasks]
        self.assertIn(1, task_ids)
        self.assertIn(3, task_ids)
        self.assertNotIn(2, task_ids)


class TestHandleUpdate(unittest.TestCase):
    """Test handle_update command integration."""

    def setUp(self):
        """Create fresh TaskManager with sample tasks."""
        self.manager = TaskManager()
        self.task1 = self.manager.add_task("Original Title 1", "Original Description 1")
        self.task2 = self.manager.add_task("Original Title 2", "Original Description 2")

    @patch("builtins.input", side_effect=["1", "New Title", "New Description"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_update_both_title_and_description(self, mock_stdout, mock_input):
        """Should update both title and description when provided."""
        from src.commands import handle_update
        handle_update(self.manager)

        output = mock_stdout.getvalue()
        # Should show success message
        self.assertIn("✓", output)
        self.assertIn("updated", output.lower())

        # Task should be updated
        task = self.manager.get_task_by_id(1)
        self.assertEqual(task.title, "New Title")
        self.assertEqual(task.description, "New Description")

    @patch("builtins.input", side_effect=["1", "Just New Title", ""])
    @patch("sys.stdout", new_callable=StringIO)
    def test_update_title_only(self, mock_stdout, mock_input):
        """Should update only title when description is empty."""
        from src.commands import handle_update
        handle_update(self.manager)

        task = self.manager.get_task_by_id(1)
        self.assertEqual(task.title, "Just New Title")
        # Description should remain unchanged
        self.assertEqual(task.description, "Original Description 1")

    @patch("builtins.input", side_effect=["1", "", "Just New Description"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_update_description_only(self, mock_stdout, mock_input):
        """Should update only description when title is empty."""
        from src.commands import handle_update
        handle_update(self.manager)

        task = self.manager.get_task_by_id(1)
        # Title should remain unchanged
        self.assertEqual(task.title, "Original Title 1")
        self.assertEqual(task.description, "Just New Description")

    @patch("builtins.input", side_effect=["999", "New Title", "New Description"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_update_nonexistent_task_shows_error(self, mock_stdout, mock_input):
        """Should show error for non-existent task ID."""
        from src.commands import handle_update
        handle_update(self.manager)

        output = mock_stdout.getvalue()
        self.assertIn("Error:", output)
        self.assertIn("999", output)

    @patch("builtins.input", side_effect=["abc", "New Title", "New Description"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_update_invalid_id_format_shows_error(self, mock_stdout, mock_input):
        """Should show error for invalid ID format."""
        from src.commands import handle_update
        handle_update(self.manager)

        output = mock_stdout.getvalue()
        self.assertIn("Error:", output)
        output_lower = output.lower()
        self.assertTrue("invalid" in output_lower or "format" in output_lower)

    @patch("builtins.input", side_effect=["1", "   ", ""])
    @patch("sys.stdout", new_callable=StringIO)
    def test_update_empty_title_shows_error(self, mock_stdout, mock_input):
        """Should show error when trying to set empty title (T046)."""
        from src.commands import handle_update
        handle_update(self.manager)

        output = mock_stdout.getvalue()
        self.assertIn("Error:", output)
        self.assertIn("empty", output.lower())

        # Task should remain unchanged
        task = self.manager.get_task_by_id(1)
        self.assertEqual(task.title, "Original Title 1")

    @patch("builtins.input", side_effect=["2", "Updated Task 2", "Updated Description 2"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_update_shows_task_title_in_feedback(self, mock_stdout, mock_input):
        """Should show task title in success message."""
        from src.commands import handle_update
        handle_update(self.manager)

        output = mock_stdout.getvalue()
        # Should mention the task ID in feedback
        self.assertIn("#2", output)


class TestPerformance(unittest.TestCase):
    """Test application performance with large datasets."""

    def test_performance_with_100_plus_tasks(self):
        """Application should handle 100+ tasks efficiently (T069)."""
        import time
        manager = TaskManager()

        # Add 150 tasks
        start_time = time.time()
        for i in range(150):
            manager.add_task(f"Task {i+1}", f"Description for task {i+1}")
        add_time = time.time() - start_time

        # List all tasks
        start_time = time.time()
        tasks = manager.get_all_tasks()
        list_time = time.time() - start_time

        # Update a task in the middle
        start_time = time.time()
        manager.update_task(75, title="Updated Task 75")
        update_time = time.time() - start_time

        # Mark a task as complete
        start_time = time.time()
        manager.toggle_status(100)
        toggle_time = time.time() - start_time

        # Delete a task
        start_time = time.time()
        manager.delete_task(50)
        delete_time = time.time() - start_time

        # Verify all operations completed
        self.assertEqual(len(manager.get_all_tasks()), 149)  # 150 - 1 deleted

        # All operations should be under 1 second (per requirements)
        self.assertLess(add_time, 1.0, "Adding 150 tasks should take < 1 second")
        self.assertLess(list_time, 1.0, "Listing tasks should take < 1 second")
        self.assertLess(update_time, 1.0, "Updating task should take < 1 second")
        self.assertLess(toggle_time, 1.0, "Toggling status should take < 1 second")
        self.assertLess(delete_time, 1.0, "Deleting task should take < 1 second")


class TestFullLifecycle(unittest.TestCase):
    """Test complete task lifecycle: add → view → update → complete → delete (T070)."""

    @patch("builtins.input", side_effect=[
        # Add task
        "Buy groceries", "Milk, eggs, bread",
        # Update task
        "1", "Buy groceries and snacks", "Milk, eggs, bread, chips",
        # Mark as complete
        "1",
        # Delete task
        "1"
    ])
    @patch("sys.stdout", new_callable=StringIO)
    def test_complete_task_lifecycle(self, mock_stdout, mock_input):
        """Complete lifecycle: add → view → update → mark → delete."""
        from src.commands import handle_add, handle_list, handle_update, handle_mark, handle_delete
        manager = TaskManager()

        # Step 1: Add a task
        handle_add(manager)
        tasks = manager.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Buy groceries")
        self.assertEqual(tasks[0].description, "Milk, eggs, bread")
        self.assertEqual(tasks[0].status.value, "Pending")

        # Step 2: View tasks
        handle_list(manager)
        output = mock_stdout.getvalue()
        self.assertIn("Buy groceries", output)

        # Step 3: Update the task
        handle_update(manager)
        task = manager.get_task_by_id(1)
        self.assertEqual(task.title, "Buy groceries and snacks")
        self.assertEqual(task.description, "Milk, eggs, bread, chips")

        # Step 4: Mark as complete
        handle_mark(manager)
        task = manager.get_task_by_id(1)
        self.assertEqual(task.status.value, "Completed")

        # Step 5: Delete the task
        handle_delete(manager)
        tasks = manager.get_all_tasks()
        self.assertEqual(len(tasks), 0)
        self.assertIsNone(manager.get_task_by_id(1))

    def test_multiple_tasks_lifecycle(self):
        """Test managing multiple tasks through full lifecycle."""
        manager = TaskManager()

        # Add multiple tasks
        task1 = manager.add_task("Task 1", "Description 1")
        task2 = manager.add_task("Task 2", "Description 2")
        task3 = manager.add_task("Task 3", "Description 3")

        # Update task 2
        manager.update_task(2, title="Updated Task 2")
        self.assertEqual(manager.get_task_by_id(2).title, "Updated Task 2")

        # Mark task 1 and 3 as complete
        manager.toggle_status(1)
        manager.toggle_status(3)
        self.assertEqual(manager.get_task_by_id(1).status.value, "Completed")
        self.assertEqual(manager.get_task_by_id(3).status.value, "Completed")

        # Delete task 2
        manager.delete_task(2)
        tasks = manager.get_all_tasks()
        self.assertEqual(len(tasks), 2)

        # Verify remaining tasks
        task_ids = [t.id for t in tasks]
        self.assertIn(1, task_ids)
        self.assertIn(3, task_ids)
        self.assertNotIn(2, task_ids)


if __name__ == "__main__":
    unittest.main()
