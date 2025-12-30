# CLI Command Contracts

**Feature**: 001-todo-inmemory-app
**Date**: 2025-12-29
**Interface Type**: Command-line REPL

## Overview

This document defines the contract for all CLI commands supported by the Todo application. Each command specifies its syntax, inputs, outputs, and error conditions.

## General Command Format

```
<command> [arguments]
```

**Conventions**:
- Commands are case-insensitive
- Arguments are space-separated
- Interactive prompts used when arguments not provided inline

## Command Reference

### 1. add

**Purpose**: Create a new task with title and optional description

**Syntax**:
```
add
```

**Input Flow**:
1. Command entered
2. System prompts: "Enter task title: "
3. User enters title
4. System prompts: "Enter task description (optional, press Enter to skip): "
5. User enters description or presses Enter

**Success Output**:
```
✓ Task <id> created successfully
```

**Error Conditions**:

| Error Case             | User Input Example | Error Message                    |
|------------------------|-------------------|----------------------------------|
| Empty title            | ""                | "Error: Title cannot be empty"   |
| Whitespace-only title  | "   "             | "Error: Title cannot be empty"   |

**Mapping**: FR-001, FR-002, FR-003, FR-004

---

### 2. list

**Purpose**: Display all tasks in a formatted table

**Syntax**:
```
list
```

**Success Output** (with tasks):
```
ID | Title                    | Status    | Description
---+--------------------------+-----------+---------------------------
 1 | Buy groceries            | [ ] Pend. | Get milk, eggs, bread
 2 | Call dentist             | [✓] Comp. | Schedule annual checkup
 3 | Team meeting             | [ ] Pend. | Prepare slides for presen...
```

**Success Output** (no tasks):
```
No tasks yet. Add your first task to get started!
```

**Error Conditions**: None (always succeeds)

**Mapping**: FR-005, FR-006, FR-007

**Display Rules**:
- ID: Right-aligned, width 3
- Title: Left-aligned, width 25, truncated with "..." if longer
- Status: Fixed width 10, format "[ ] Pend." or "[✓] Comp."
- Description: Left-aligned, width 50, truncated with "..." if longer

---

### 3. update

**Purpose**: Modify title and/or description of an existing task

**Syntax**:
```
update <task_id>
```

**Input Flow**:
1. Command entered with task ID
2. System prompts: "Enter new title (leave blank to keep current): "
3. User enters new title or presses Enter
4. System prompts: "Enter new description (leave blank to keep current): "
5. User enters new description or presses Enter

**Success Output**:
```
✓ Task <id> updated successfully
```

**Error Conditions**:

| Error Case           | User Input Example | Error Message                           |
|----------------------|-------------------|-----------------------------------------|
| Missing task ID      | "update"          | "Error: Task ID required. Usage: update <id>" |
| Invalid ID format    | "update abc"      | "Error: Invalid task ID format: 'abc'"  |
| Task not found       | "update 999"      | "Error: Task with ID 999 not found"     |
| Empty new title      | "" (when prompted)| "Error: Title cannot be empty"          |
| Whitespace-only title| "   "             | "Error: Title cannot be empty"          |

**Mapping**: FR-008, FR-009, FR-010, FR-015

---

### 4. delete

**Purpose**: Permanently remove a task

**Syntax**:
```
delete <task_id>
```

**Success Output**:
```
✓ Task <id> deleted successfully
```

**Error Conditions**:

| Error Case        | User Input Example | Error Message                            |
|-------------------|-------------------|------------------------------------------|
| Missing task ID   | "delete"          | "Error: Task ID required. Usage: delete <id>" |
| Invalid ID format | "delete xyz"      | "Error: Invalid task ID format: 'xyz'"   |
| Task not found    | "delete 999"      | "Error: Task with ID 999 not found"      |

**Mapping**: FR-011, FR-012, FR-015, FR-019

**Note**: Task IDs are not reused after deletion

---

### 5. complete

**Purpose**: Toggle task status between Pending and Completed

**Syntax**:
```
complete <task_id>
```

**Aliases**: `toggle <task_id>`

**Success Output** (when marking complete):
```
✓ Task <id> marked as Completed
```

**Success Output** (when marking incomplete):
```
✓ Task <id> marked as Pending
```

**Error Conditions**:

| Error Case        | User Input Example | Error Message                             |
|-------------------|-------------------|-------------------------------------------|
| Missing task ID   | "complete"        | "Error: Task ID required. Usage: complete <id>" |
| Invalid ID format | "complete abc"    | "Error: Invalid task ID format: 'abc'"    |
| Task not found    | "complete 999"    | "Error: Task with ID 999 not found"       |

**Mapping**: FR-013, FR-014, FR-015

---

### 6. help

**Purpose**: Display available commands and usage examples

**Syntax**:
```
help
```

**Output**:
```
Available Commands:
-------------------
add              Create a new task
list             Show all tasks
update <id>      Update a task's title and/or description
delete <id>      Delete a task permanently
complete <id>    Toggle task completion status
help             Show this help message
exit, quit       Exit the application

Examples:
---------
add              → Creates a new task (prompts for details)
list             → Shows all tasks in a table
update 1         → Updates task #1 (prompts for new values)
delete 2         → Deletes task #2
complete 3       → Toggles completion status of task #3

Tips:
-----
• Task IDs are shown in the 'list' view
• Descriptions are optional when creating tasks
• Empty titles are not allowed
```

**Error Conditions**: None (always succeeds)

**Mapping**: FR-018

---

### 7. exit / quit

**Purpose**: Terminate the application

**Syntax**:
```
exit
```
or
```
quit
```

**Output**:
```
Goodbye! All tasks will be lost.
```

**Error Conditions**: None (always succeeds)

**Mapping**: FR-017

**Note**: All in-memory data is lost on exit (by design)

---

## Invalid Command Handling

**Behavior**: When user enters unrecognized command

**Example Input**: `remove 5` (not a valid command)

**Output**:
```
Error: Unknown command 'remove'
Type 'help' to see available commands
```

**Mapping**: FR-016, FR-020

**Suggestions** (optional enhancement):
- If command is similar to known command, suggest: "Did you mean 'delete'?"

---

## Input Validation Rules

### General Rules (applies to all commands)

1. **Whitespace Handling**:
   - Leading/trailing whitespace trimmed from all inputs
   - Empty string after trimming considered invalid for required fields

2. **Case Sensitivity**:
   - Commands are case-insensitive (`Add`, `ADD`, `add` all accepted)
   - Title and description preserve user's case

3. **Special Characters**:
   - All UTF-8 characters allowed in title and description
   - No special character escaping required

4. **Length Limits**:
   - No hard limit on title or description length
   - Display truncation only (data preserved in full)

### Task ID Validation

```python
def validate_task_id(input: str) -> int:
    """
    Validates task ID input

    Args:
        input: User input string

    Returns:
        int: Validated task ID

    Raises:
        ValueError: If input is not a valid integer or task not found
    """
    # Check numeric format
    if not input.strip().isdigit():
        raise ValueError(f"Invalid task ID format: '{input}'")

    # Convert to integer
    task_id = int(input.strip())

    # Check existence (handled by TaskManager)
    # Raises ValueError if not found

    return task_id
```

### Title Validation

```python
def validate_title(input: str) -> str:
    """
    Validates task title

    Args:
        input: User input string

    Returns:
        str: Validated and normalized title

    Raises:
        ValueError: If title is empty or whitespace-only
    """
    cleaned = input.strip()
    if not cleaned:
        raise ValueError("Title cannot be empty")
    return cleaned
```

## Response Time Requirements

**From SC-008**: All operations must provide feedback in under 1 second

**Expected Response Times**:
- `add`: < 100ms
- `list`: < 100ms (for 100 tasks)
- `update`: < 100ms
- `delete`: < 100ms
- `complete`: < 100ms
- `help`: < 50ms
- `exit`: < 50ms

All times well within 1-second requirement.

## Error Message Format

**Standard Format**:
```
Error: <clear description of what went wrong>
[Optional: Suggestion for how to fix it]
```

**Examples**:
```
Error: Invalid task ID format: 'abc'
Error: Task with ID 999 not found
Error: Title cannot be empty
Error: Task ID required. Usage: delete <id>
Error: Unknown command 'remove'
Type 'help' to see available commands
```

**Mapping**: FR-016, SC-005

## Session Lifecycle

```
[Application Start]
    ↓
Display welcome message
Initialize empty task list
    ↓
[Main Loop]
    ↓
Prompt: "todo> "
Read command
Parse and validate
Execute command
Display output/error
    ↓
Repeat until 'exit' or 'quit'
    ↓
[Application Exit]
Display goodbye message
Terminate (all data lost)
```

## Contract Testing

Each command contract should be tested with:
1. **Happy path**: Valid input produces expected output
2. **Edge cases**: Boundary conditions (empty, very long, special chars)
3. **Error cases**: Each error condition triggers correct error message
4. **Performance**: Response time under 1 second

Example test cases documented in acceptance scenarios (spec.md).
