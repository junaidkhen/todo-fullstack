"""Main entry point for Todo In-Memory Console App."""

import sys
from src.task_manager import TaskManager
from src.commands import handle_add, handle_list, handle_mark, handle_update, handle_delete, handle_help


def main() -> None:
    """Run the Todo application REPL (Read-Eval-Print Loop)."""
    # Initialize task manager
    manager = TaskManager()

    # Display welcome message
    print("Welcome to Todo App!")
    print("Type 'help' for available commands.")
    print()

    # Main REPL loop
    while True:
        try:
            # Get user input
            user_input = input("todo> ").strip()

            # Skip empty input
            if not user_input:
                continue

            # Parse command (convert to lowercase for case-insensitive matching)
            command = user_input.lower()

            # Handle exit commands
            if command in ["exit", "quit"]:
                print("Goodbye! All tasks will be lost.")
                sys.exit(0)

            # Handle help command
            elif command == "help":
                handle_help()

            # Handle add command
            elif command == "add":
                handle_add(manager)

            # Handle list command
            elif command == "list":
                handle_list(manager)

            # Handle mark command
            elif command == "mark":
                handle_mark(manager)

            # Handle update command
            elif command == "update":
                handle_update(manager)

            # Handle delete command
            elif command == "delete":
                handle_delete(manager)

            # Handle unknown commands
            else:
                print(f"Error: Unknown command '{user_input}'")
                print("Type 'help' to see available commands")

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nGoodbye! All tasks will be lost.")
            sys.exit(0)
        except EOFError:
            # Handle Ctrl+D gracefully
            print("\nGoodbye! All tasks will be lost.")
            sys.exit(0)


if __name__ == "__main__":
    main()
