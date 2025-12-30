# Todo In-Memory Console App

A simple command-line todo list application that stores tasks in memory. Perfect for quick task tracking during your work session.

## Features

- ✅ **Add Tasks** - Create tasks with title and optional description
- ✅ **View Tasks** - Display all tasks in a formatted table
- ✅ **Mark Complete** - Toggle tasks between pending and completed status
- ✅ **Update Tasks** - Modify task title and/or description
- ✅ **Delete Tasks** - Permanently remove tasks
- ✅ **In-Memory Storage** - Fast, lightweight (data clears on exit)

## Requirements

- Python 3.13 or higher
- No external dependencies (uses Python standard library only)

## Installation

1. Clone or download this repository
2. Navigate to the backend directory:
   ```bash
   cd todo/Todo-app
   ```

No additional installation steps needed!

## Usage

### Starting the Application

Run the application using Python:

```bash
python3 -m src.main
```

You'll see a welcome message:
```
Welcome to Todo App!
Type 'help' for available commands.

todo>
```

### Available Commands

| Command | Description |
|---------|-------------|
| `add` | Add a new task |
| `list` | View all tasks |
| `mark` | Mark a task as complete/incomplete |
| `update` | Update a task's title or description |
| `delete` | Delete a task |
| `help` | Show available commands |
| `exit` or `quit` | Exit the application |

### Example Session

```
todo> add
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread
✓ Task #1 added: Buy groceries

todo> add
Enter task title: Write report
Enter task description (optional): Q4 financial summary
✓ Task #2 added: Write report

todo> list
┌────┬──────────────────────────┬──────────────┬─────────────────────────────────────────────────────┐
│ ID │ Title                    │ Status       │ Description                                         │
├────┼──────────────────────────┼──────────────┼─────────────────────────────────────────────────────┤
│ 1  │ Buy groceries            │ [ ] Pend.    │ Milk, eggs, bread                                   │
│ 2  │ Write report             │ [ ] Pend.    │ Q4 financial summary                                │
└────┴──────────────────────────┴──────────────┴─────────────────────────────────────────────────────┘

todo> mark
Enter task ID to mark: 1
✓ Task #1 'Buy groceries' marked as completed

todo> list
┌────┬──────────────────────────┬──────────────┬─────────────────────────────────────────────────────┐
│ ID │ Title                    │ Status       │ Description                                         │
├────┼──────────────────────────┼──────────────┼─────────────────────────────────────────────────────┤
│ 1  │ Buy groceries            │ [✓] Comp.    │ Milk, eggs, bread                                   │
│ 2  │ Write report             │ [ ] Pend.    │ Q4 financial summary                                │
└────┴──────────────────────────┴──────────────┴─────────────────────────────────────────────────────┘

todo> update
Enter task ID to update: 2
Enter new title (leave empty to keep current): Write Q4 Report
Enter new description (leave empty to keep current): Financial summary with charts
✓ Task #2 updated successfully

todo> delete
Enter task ID to delete: 1
✓ Task #1 'Buy groceries' deleted successfully

todo> exit
Goodbye! All tasks will be lost.
```

## Project Structure

```
todo/
├── Todo-app/              # Backend application
│   ├── src/
│   │   ├── __init__.py         # Package marker
│   │   ├── main.py             # Entry point and REPL loop
│   │   ├── models.py           # Task and TaskStatus definitions
│   │   ├── task_manager.py     # Core business logic
│   │   ├── commands.py         # Command handlers
│   │   ├── display.py          # Output formatting
│   │   └── validation.py       # Input validation
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_task_manager.py
│   │   ├── test_commands.py
│   │   ├── test_validation.py
│   │   ├── test_display.py
│   │   └── test_integration.py
│   ├── .venv/             # Virtual environment
│   ├── demo_app.py        # Demo script
│   ├── pyproject.toml     # Project configuration
│   └── requirements.md    # Requirements documentation
├── README.md              # Project documentation
└── TESTING_REPORT.md      # Testing report
```

## Running Tests

Run all tests:
```bash
python3 -m unittest discover tests -v
```

Run specific test module:
```bash
python3 -m unittest tests.test_task_manager -v
```

Expected output: **114 tests, all passing**

## Technical Details

### Architecture

- **Clean Architecture**: Separation of concerns with distinct layers
  - Models: Data structures (Task, TaskStatus)
  - Business Logic: TaskManager for CRUD operations
  - Commands: User interface handlers
  - Display: Output formatting
  - Validation: Input sanitization

- **Type Safety**: Full type hints throughout codebase
- **Error Handling**: Comprehensive validation with clear error messages
- **Testing**: 114 unit and integration tests with full coverage

### Design Decisions

1. **In-Memory Storage**: Uses Python list for fast operations
2. **ID Management**: Auto-incrementing IDs that are never reused
3. **Data Validation**: Input validation at command handler level
4. **Display Formatting**: Fixed-width ASCII tables with truncation
5. **Performance**: All operations complete in < 1 second (tested with 150 tasks)

### Limitations

- **No Persistence**: Tasks are lost when application exits
- **Single User**: Designed for individual use
- **No Editing History**: No undo/redo functionality
- **Basic Formatting**: Simple ASCII tables (no color support)

## Development

### Code Quality

- ✅ PEP 8 compliant
- ✅ Type hints on all public functions
- ✅ Comprehensive docstrings
- ✅ 114 passing tests
- ✅ No external dependencies

### Adding New Features

1. Update data model in `src/models.py` if needed
2. Add business logic to `src/task_manager.py`
3. Create command handler in `src/commands.py`
4. Wire command in `src/main.py`
5. Write tests in `tests/`
6. Update this README

## Troubleshooting

**Q: Application doesn't start**
- Ensure Python 3.13+ is installed: `python3 --version`
- Run from the correct directory (where src/ folder is located)

**Q: Tasks disappeared**
- This is expected! Tasks are stored in memory only and are cleared when you exit

**Q: Command not recognized**
- Type `help` to see all available commands
- Commands are case-insensitive

**Q: Can't update/delete a task**
- Verify the task ID with `list` command first
- Task IDs are permanent and never reused

## License

This project was created as part of a coding exercise. Feel free to use and modify as needed.

## Contributing

This is a demonstration project. For learning purposes, try:
- Adding file persistence (JSON, SQLite)
- Implementing task priorities
- Adding due dates and reminders
- Creating a graphical user interface
- Adding task categories/tags

## Credits

Built with Python 3.13+ using Test-Driven Development (TDD) methodology.
Developed following Spec-Driven Development practices.
"# todo" 
