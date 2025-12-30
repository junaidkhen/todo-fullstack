# Quickstart Guide: Todo In-Memory Console App

**Feature**: 001-todo-inmemory-app
**Last Updated**: 2025-12-29

## Prerequisites

- Python 3.13 or higher
- No external dependencies required (uses Python standard library only)

## Installation

### Option 1: Clone and Run (Development)

```bash
# Clone the repository
git clone <repository-url>
cd todo

# Verify Python version
python --version  # Should show 3.13 or higher

# Run the application directly
python src/main.py
```

### Option 2: Using UV (Recommended for Development)

```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install
cd todo
uv sync

# Run the application
uv run python src/main.py
```

## Quick Start

1. **Start the application**:
   ```bash
   python src/main.py
   ```

2. **You'll see the welcome prompt**:
   ```
   Welcome to Todo App!
   Type 'help' for available commands.

   todo>
   ```

3. **Add your first task**:
   ```
   todo> add
   Enter task title: Buy groceries
   Enter task description (optional, press Enter to skip): Milk, eggs, bread
   ✓ Task 1 created successfully
   ```

4. **View all tasks**:
   ```
   todo> list
   ID | Title                    | Status    | Description
   ---+--------------------------+-----------+---------------------------
    1 | Buy groceries            | [ ] Pend. | Milk, eggs, bread
   ```

5. **Mark task as complete**:
   ```
   todo> complete 1
   ✓ Task 1 marked as Completed
   ```

6. **Exit the application**:
   ```
   todo> exit
   Goodbye! All tasks will be lost.
   ```

## Available Commands

| Command        | Description                              | Example          |
|----------------|------------------------------------------|------------------|
| `add`          | Create a new task                        | `add`            |
| `list`         | Show all tasks                           | `list`           |
| `update <id>`  | Update task title and/or description     | `update 1`       |
| `delete <id>`  | Delete a task permanently                | `delete 2`       |
| `complete <id>`| Toggle task completion status            | `complete 3`     |
| `help`         | Show help message with all commands      | `help`           |
| `exit` / `quit`| Exit the application                     | `exit`           |

## Usage Examples

### Creating Tasks

```
todo> add
Enter task title: Call dentist
Enter task description (optional, press Enter to skip): Schedule annual checkup
✓ Task 1 created successfully

todo> add
Enter task title: Team meeting
Enter task description (optional, press Enter to skip):
✓ Task 2 created successfully
```

### Viewing Tasks

```
todo> list
ID | Title                    | Status    | Description
---+--------------------------+-----------+---------------------------
 1 | Call dentist             | [ ] Pend. | Schedule annual checkup
 2 | Team meeting             | [ ] Pend. |
```

### Updating Tasks

```
todo> update 2
Enter new title (leave blank to keep current): Team Meeting at 3pm
Enter new description (leave blank to keep current): Prepare presentation slides
✓ Task 2 updated successfully

todo> list
ID | Title                    | Status    | Description
---+--------------------------+-----------+---------------------------
 1 | Call dentist             | [ ] Pend. | Schedule annual checkup
 2 | Team Meeting at 3pm      | [ ] Pend. | Prepare presentation slides
```

### Completing Tasks

```
todo> complete 1
✓ Task 1 marked as Completed

todo> list
ID | Title                    | Status    | Description
---+--------------------------+-----------+---------------------------
 1 | Call dentist             | [✓] Comp. | Schedule annual checkup
 2 | Team Meeting at 3pm      | [ ] Pend. | Prepare presentation slides

# Toggle back to pending
todo> complete 1
✓ Task 1 marked as Pending
```

### Deleting Tasks

```
todo> delete 1
✓ Task 1 deleted successfully

todo> list
ID | Title                    | Status    | Description
---+--------------------------+-----------+---------------------------
 2 | Team Meeting at 3pm      | [ ] Pend. | Prepare presentation slides

# Note: Task IDs are not reused after deletion
```

## Common Error Examples

### Empty Title
```
todo> add
Enter task title:
Error: Title cannot be empty
```

### Invalid Task ID
```
todo> update abc
Error: Invalid task ID format: 'abc'

todo> delete 999
Error: Task with ID 999 not found
```

### Unknown Command
```
todo> remove 1
Error: Unknown command 'remove'
Type 'help' to see available commands
```

## Tips

1. **Task IDs are permanent**: Once a task is deleted, its ID is never reused
2. **Data is temporary**: All tasks are lost when you exit the application (by design)
3. **No character limits**: You can enter very long titles and descriptions (they'll be truncated in the list view)
4. **Empty descriptions are OK**: You don't need to provide a description when creating tasks
5. **Case doesn't matter**: Commands work regardless of case (`add`, `Add`, `ADD` all work)

## Troubleshooting

### "python: command not found"
- Make sure Python 3.13+ is installed
- Try `python3` instead of `python`
- On Windows, you may need to add Python to your PATH

### "ModuleNotFoundError"
- This application uses only Python standard library
- If you see this error, verify your Python installation

### Application crashes on invalid input
- This shouldn't happen! All invalid inputs should show error messages
- If you encounter a crash, this is a bug - please report it

### Tasks disappear after closing
- This is expected behavior
- The application stores tasks in memory only (no persistence)
- All data is lost when the application exits

## Development

### Running Tests

```bash
# Using pytest (if installed)
pytest tests/

# Using built-in unittest
python -m unittest discover tests/
```

### Project Structure

```
todo/
├── src/
│   ├── __init__.py
│   ├── main.py           # Entry point, CLI loop
│   ├── models.py         # Task, TaskStatus definitions
│   ├── task_manager.py   # TaskManager class
│   ├── commands.py       # Command handlers
│   ├── display.py        # Output formatting
│   └── validation.py     # Input validation
├── tests/
│   ├── test_models.py
│   ├── test_task_manager.py
│   ├── test_commands.py
│   └── test_validation.py
├── README.md
└── pyproject.toml
```

### Code Standards

- Python 3.13+
- PEP 8 compliant
- Type hints required
- No external dependencies
- Comprehensive input validation

## Performance

- Handles 100+ tasks without noticeable performance degradation
- All operations respond in under 1 second
- Typical operation times:
  - Add task: < 100ms
  - List tasks: < 100ms
  - Update/Delete/Complete: < 100ms

## Known Limitations

1. **No persistence**: Data is lost on exit (intentional design)
2. **No multi-user support**: Single-user, single-session only
3. **No undo/redo**: Operations are permanent (except toggle complete)
4. **No task search**: Must scroll through list to find tasks
5. **No task filtering**: Cannot filter by status or other criteria
6. **Display truncation**: Long titles/descriptions truncated in list view

These limitations are by design for Phase I (Basic Level). Future phases may add these features.

## Getting Help

1. **In-app help**: Type `help` at the prompt
2. **Documentation**: See `specs/001-todo-inmemory-app/` for detailed design docs
3. **Code reference**: Check inline comments and docstrings in source files

## Next Steps

After getting familiar with the application:
1. Review the [specification](spec.md) to understand requirements
2. Check [data-model.md](data-model.md) for entity definitions
3. Read [contracts/cli-commands.md](contracts/cli-commands.md) for command details
4. Explore the source code to understand implementation

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
