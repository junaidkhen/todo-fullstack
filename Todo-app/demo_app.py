#!/usr/bin/env python3
"""Demonstration script for Todo In-Memory Console App.

This script simulates a user session to demonstrate all features.
"""

import sys
from io import StringIO
from src.task_manager import TaskManager
from src.commands import (
    handle_add, handle_list, handle_mark,
    handle_update, handle_delete, handle_help
)


def demo_session():
    """Run a demonstration session showcasing all features."""

    print("=" * 80)
    print("TODO IN-MEMORY CONSOLE APP - DEMONSTRATION")
    print("=" * 80)
    print()

    # Initialize TaskManager
    manager = TaskManager()

    # Demo 1: Show help
    print("📋 DEMO 1: Help Command")
    print("-" * 80)
    handle_help()
    print()

    # Demo 2: Add tasks
    print("📋 DEMO 2: Adding Tasks")
    print("-" * 80)
    print("Adding 3 tasks...")
    task1 = manager.add_task("Buy groceries", "Milk, eggs, bread, and butter")
    print(f"✓ Added: Task #{task1.id} - {task1.title}")

    task2 = manager.add_task("Write report", "Q4 financial summary with charts")
    print(f"✓ Added: Task #{task2.id} - {task2.title}")

    task3 = manager.add_task("Call dentist", "Schedule annual checkup")
    print(f"✓ Added: Task #{task3.id} - {task3.title}")
    print()

    # Demo 3: List all tasks
    print("📋 DEMO 3: Viewing All Tasks")
    print("-" * 80)
    handle_list(manager)
    print()

    # Demo 4: Mark task as complete
    print("📋 DEMO 4: Marking Task as Complete")
    print("-" * 80)
    print(f"Marking task #{task1.id} as complete...")
    manager.toggle_status(task1.id)
    print(f"✓ Task #{task1.id} '{task1.title}' marked as completed")
    print("\nUpdated task list:")
    handle_list(manager)
    print()

    # Demo 5: Update a task
    print("📋 DEMO 5: Updating Task Details")
    print("-" * 80)
    print(f"Updating task #{task2.id}...")
    manager.update_task(task2.id, title="Write Q4 Report",
                       description="Financial summary with charts and projections")
    updated_task = manager.get_task_by_id(task2.id)
    print(f"✓ Updated: Task #{updated_task.id}")
    print(f"  New title: {updated_task.title}")
    print(f"  New description: {updated_task.description}")
    print("\nUpdated task list:")
    handle_list(manager)
    print()

    # Demo 6: Mark another task as complete
    print("📋 DEMO 6: Marking Another Task Complete")
    print("-" * 80)
    print(f"Marking task #{task3.id} as complete...")
    manager.toggle_status(task3.id)
    print(f"✓ Task #{task3.id} '{task3.title}' marked as completed")
    print("\nUpdated task list:")
    handle_list(manager)
    print()

    # Demo 7: Toggle task back to pending
    print("📋 DEMO 7: Toggle Task Back to Pending")
    print("-" * 80)
    print(f"Toggling task #{task3.id} back to pending...")
    manager.toggle_status(task3.id)
    print(f"✓ Task #{task3.id} '{task3.title}' marked as pending")
    print("\nUpdated task list:")
    handle_list(manager)
    print()

    # Demo 8: Delete a task
    print("📋 DEMO 8: Deleting a Task")
    print("-" * 80)
    print(f"Deleting task #{task1.id}...")
    deleted_title = task1.title
    manager.delete_task(task1.id)
    print(f"✓ Task #{task1.id} '{deleted_title}' deleted successfully")
    print("\nUpdated task list:")
    handle_list(manager)
    print()

    # Demo 9: Add more tasks to show ID stability
    print("📋 DEMO 9: ID Stability (IDs Never Reused)")
    print("-" * 80)
    print("Adding a new task after deletion...")
    task4 = manager.add_task("Prepare presentation", "Team meeting slides")
    print(f"✓ Added: Task #{task4.id} - {task4.title}")
    print(f"\n⚠️  Notice: New task has ID #{task4.id}, NOT #{task1.id} (deleted ID is never reused)")
    print("\nFinal task list:")
    handle_list(manager)
    print()

    # Demo 10: Performance with many tasks
    print("📋 DEMO 10: Performance Test (Adding 100 Tasks)")
    print("-" * 80)
    import time

    start_time = time.time()
    for i in range(100):
        manager.add_task(f"Task {i+10}", f"Description for task {i+10}")
    elapsed_time = time.time() - start_time

    print(f"✓ Added 100 tasks in {elapsed_time:.4f} seconds")
    print(f"📊 Total tasks in system: {len(manager.get_all_tasks())}")

    # Show first few and last few
    all_tasks = manager.get_all_tasks()
    print(f"\nShowing first 3 and last 3 of {len(all_tasks)} tasks:")
    print(f"  First: #{all_tasks[0].id} - {all_tasks[0].title}")
    print(f"  ...{len(all_tasks) - 4} more tasks...")
    print(f"  Last:  #{all_tasks[-1].id} - {all_tasks[-1].title}")
    print()

    # Summary
    print("=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print()
    print("✅ All features demonstrated:")
    print("   • Add tasks (with title and description)")
    print("   • View tasks (formatted table)")
    print("   • Mark tasks complete/pending (toggle)")
    print("   • Update task details (title and/or description)")
    print("   • Delete tasks (with ID stability)")
    print("   • Help command")
    print("   • Performance with 100+ tasks")
    print()
    print(f"📊 Final Statistics:")
    print(f"   • Total tasks created: {manager._next_id - 1}")
    print(f"   • Active tasks: {len(all_tasks)}")
    print(f"   • All operations completed successfully!")
    print()
    print("💡 To run the application interactively:")
    print("   .venv/bin/python3 -m src.main")
    print()


if __name__ == "__main__":
    demo_session()
