# Research: Todo In-Memory Console App

**Feature**: 001-todo-inmemory-app
**Date**: 2025-12-29
**Purpose**: Resolve technical unknowns and establish architectural decisions

## Research Items

### 1. Python Version and Standard Library Capabilities

**Decision**: Python 3.13+ with standard library only

**Rationale**:
- Python 3.13 provides latest dataclasses features with improved performance
- Standard library includes all necessary modules:
  - `dataclasses` for Task entity definition
  - `typing` for type hints
  - `enum` for status enumeration
  - `sys` for CLI input/output
  - No external dependencies needed for in-memory storage

**Alternatives Considered**:
- Python 3.11/3.12: Considered but 3.13 specified in user requirements
- External libraries (e.g., Click, Rich): Rejected per "no external dependencies" constraint

### 2. Command-Line Interface Pattern

**Decision**: Simple command-based REPL (Read-Eval-Print Loop) with text parsing

**Rationale**:
- Intuitive for users: natural language-like commands (e.g., "add", "list", "update 1")
- Zero dependencies: uses built-in `input()` function
- Easy to extend with new commands
- Clear separation between command parsing and business logic

**Alternatives Considered**:
- argparse-based CLI: Rejected because requires restarting app for each command
- Menu-driven interface: Considered but less efficient for experienced users
- Click/Typer frameworks: Rejected per "no external dependencies" constraint

**Command Format**:
```
add                    # Prompts for title and description
list                   # Shows all tasks
update <id>            # Prompts for new title/description
delete <id>            # Deletes task by ID
complete <id>          # Toggles completion status
help                   # Shows available commands
exit/quit              # Exits application
```

### 3. Data Structure for In-Memory Storage

**Decision**: Python list with Task dataclass objects

**Rationale**:
- Simple and efficient for small-to-medium datasets (spec requires handling 100+ tasks)
- Dataclass provides type safety, immutability options, and clean syntax
- List maintains insertion order (useful for displaying tasks)
- O(n) lookup by ID is acceptable for 100 tasks (< 1ms)
- Easy to iterate for list operations

**Alternatives Considered**:
- Dictionary with ID as key: Considered but list is simpler and order is preserved
- NamedTuple: Rejected because dataclass provides better type hints and mutability control
- Plain dict objects: Rejected because dataclass provides better IDE support and validation

**Implementation Approach**:
```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class TaskStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"

@dataclass
class Task:
    id: int
    title: str
    description: str
    status: TaskStatus
```

### 4. ID Generation Strategy

**Decision**: Simple counter starting at 1, never decremented on deletion

**Rationale**:
- Meets requirement FR-003: "automatically assign unique, auto-incrementing integer ID"
- Meets requirement FR-019: "maintain stable task IDs (no re-numbering when tasks are deleted)"
- Simple to implement with a single integer variable
- No gaps in sequence initially, but gaps appear after deletions (acceptable per spec)

**Alternatives Considered**:
- UUID: Rejected because spec requires integer IDs
- Reuse deleted IDs: Rejected per FR-019 stability requirement
- Database-style sequences: Overkill for in-memory application

**Implementation**:
```python
class TaskManager:
    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            status=TaskStatus.PENDING
        )
        self._tasks.append(task)
        self._next_id += 1
        return task
```

### 5. Input Validation Strategy

**Decision**: Validation at command handler level with clear error messages

**Rationale**:
- Meets requirement FR-020: "validate user input for all operations and prevent crashes"
- Early validation provides immediate feedback to users (SC-008: under 1 second)
- Centralized error handling ensures consistent messaging
- Type hints catch many errors at development time

**Validation Rules**:
- Title: strip whitespace, reject if empty
- Task ID: must be numeric, must exist in task list
- Commands: match against known command list, suggest similar commands if typo

**Error Handling Pattern**:
```python
def validate_title(title: str) -> str:
    """Validates and normalizes task title."""
    cleaned = title.strip()
    if not cleaned:
        raise ValueError("Title cannot be empty")
    return cleaned

def validate_task_id(task_id: str, tasks: list[Task]) -> int:
    """Validates task ID and checks existence."""
    try:
        id_num = int(task_id)
    except ValueError:
        raise ValueError(f"Invalid task ID format: '{task_id}'")

    if not any(t.id == id_num for t in tasks):
        raise ValueError(f"Task with ID {id_num} not found")

    return id_num
```

### 6. Display Formatting and Truncation

**Decision**: Fixed-width table format with manual truncation

**Rationale**:
- No external dependencies (no tabulate, no rich)
- Clean, readable output for terminal
- Truncate description at 50 characters per FR-006
- Use simple ASCII characters for compatibility

**Format**:
```
ID | Title                    | Status    | Description
---+-------------------------+-----------+---------------------------
 1 | Buy groceries            | [ ] Pend. | Get milk, eggs, bread...
 2 | Call dentist             | [✓] Comp. | Schedule annual checkup...
```

**Alternatives Considered**:
- Rich library tables: Rejected per "no external dependencies"
- JSON output: Rejected because spec requires "readable format" for humans
- Tabulate library: Rejected per "no external dependencies"

### 7. Project Structure

**Decision**: Single project structure with clear separation of concerns

**Rationale**:
- Application is self-contained (no API, no frontend)
- Clear module separation enables testing
- Follows Python packaging best practices

**Structure**:
```
todo/
├── src/
│   ├── __init__.py
│   ├── main.py           # Entry point, CLI loop
│   ├── models.py         # Task, TaskStatus definitions
│   ├── task_manager.py   # TaskManager class
│   ├── commands.py       # Command handlers
│   ├── display.py        # Output formatting
│   └── validation.py     # Input validation utilities
├── tests/
│   ├── test_models.py
│   ├── test_task_manager.py
│   ├── test_commands.py
│   └── test_validation.py
├── README.md
└── pyproject.toml        # uv project configuration
```

### 8. Testing Strategy

**Decision**: Unit tests with pytest, no mocking for in-memory components

**Rationale**:
- pytest is part of standard development workflow (can use built-in unittest if preferred)
- In-memory components are fast enough to test directly without mocks
- Focus on behavior testing over implementation details
- Test each functional requirement directly

**Test Coverage Areas**:
- Task creation and ID assignment
- All CRUD operations
- Input validation and error cases
- Edge cases from specification
- Display formatting and truncation
- Command parsing

### 9. Performance Considerations

**Decision**: No optimization needed for initial implementation

**Rationale**:
- Spec requires handling 100 tasks (SC-004)
- Linear search through 100 items is < 1ms on modern hardware
- All operations meet SC-008 requirement (under 1 second feedback)
- Premature optimization violates YAGNI principle

**Measured Operations** (estimated for 100 tasks):
- Add task: O(1) - < 0.1ms
- List all tasks: O(n) - < 5ms including display formatting
- Find by ID: O(n) - < 0.5ms
- Update/Delete: O(n) - < 0.5ms

### 10. User Experience Enhancements

**Decision**: Clear visual indicators and helpful messages

**Rationale**:
- SC-007: "Users can identify task status instantly through clear visual indicators"
- SC-005: "100% of invalid inputs result in clear, actionable error messages"

**Enhancements**:
- Status indicators: `[ ]` for Pending, `[✓]` for Completed
- Empty state: "No tasks yet. Add your first task to get started!"
- Success messages: "Task 5 created successfully", "Task 3 marked as Completed"
- Error messages: Include what went wrong and how to fix it
- Help command: Shows all available commands with examples

## Dependencies Summary

**Language**: Python 3.13+
**Runtime Dependencies**: None (standard library only)
**Development Dependencies**: None required (pytest optional for testing)

## Risk Assessment

**Low Risk**:
- Technology stack is mature and well-documented
- No external dependencies reduces integration complexity
- In-memory storage eliminates persistence-related bugs

**Medium Risk**:
- None identified

**High Risk**:
- None identified

## Next Steps

1. Create data-model.md with detailed entity definitions
2. Create quickstart.md with setup and run instructions
3. Proceed to /sp.tasks for task breakdown
