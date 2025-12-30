#!/usr/bin/env python3
"""Interactive test simulation for Todo In-Memory Console App."""

import sys
from unittest.mock import patch
from io import StringIO


def simulate_interactive_session():
    """Simulate an interactive user session."""

    print("=" * 80)
    print("SIMULATING INTERACTIVE SESSION")
    print("=" * 80)
    print()
    print("This simulates what a user would see when running:")
    print("  .venv/bin/python3 -m src.main")
    print()
    print("-" * 80)
    print()

    # Simulate user commands
    user_inputs = [
        "help",                    # Show help
        "list",                    # List empty tasks
        "add",                     # Add first task
        "Buy groceries",           # Title
        "Milk and eggs",           # Description
        "add",                     # Add second task
        "Finish project",          # Title
        "Complete todo app",       # Description
        "list",                    # View all tasks
        "mark",                    # Mark task complete
        "1",                       # Task ID
        "list",                    # View updated list
        "update",                  # Update task
        "2",                       # Task ID
        "Finish hackathon project", # New title
        "Complete todo app demo",  # New description
        "list",                    # View updated list
        "delete",                  # Delete task
        "1",                       # Task ID
        "list",                    # View final list
        "exit"                     # Exit
    ]

    # Patch input and stdout to capture everything
    with patch('builtins.input', side_effect=user_inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            try:
                # Import and run main
                from src.main import main
                main()
            except SystemExit:
                pass  # Expected when exit is called

            # Get the output
            output = mock_stdout.getvalue()

    # Display the simulated session
    print(output)


if __name__ == "__main__":
    simulate_interactive_session()
