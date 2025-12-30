# Data Model: Todo In-Memory Console App

**Feature**: 001-todo-inmemory-app
**Date**: 2025-12-29
**Source**: Extracted from spec.md functional requirements

## Entities

### Task

**Purpose**: Represents a single todo item that users can create, view, update, complete, and delete.

**Attributes**:

| Attribute   | Type         | Required | Constraints                        | Default  |
|-------------|--------------|----------|------------------------------------|----------|
| id          | int          | Yes      | Unique, auto-increment, immutable  | Auto     |
| title       | str          | Yes      | Non-empty, non-whitespace          | -        |
| description | str          | No       | Can be empty                       | ""       |
| status      | TaskStatus   | Yes      | PENDING or COMPLETED               | PENDING  |

**Validation Rules**:

1. **Title Validation** (FR-001, FR-010):
   - MUST NOT be empty string
   - MUST NOT be only whitespace characters
   - Leading/trailing whitespace should be stripped
   - Length: No explicit limit (accept very long titles per edge cases)

2. **Description Validation** (FR-002):
   - MAY be empty string
   - No length limit (accept very long descriptions per edge cases)
   - Display truncation handled at view layer, not model layer

3. **ID Validation** (FR-003, FR-019):
   - Generated automatically on creation
   - MUST be unique across all tasks in session
   - MUST auto-increment (never reuse deleted IDs)
   - Immutable after creation

4. **Status Validation** (FR-004, FR-013):
   - Default to PENDING on creation
   - Only two valid states: PENDING or COMPLETED
   - Can toggle between states via user command

**State Transitions**:

```
[New Task]
    ↓
PENDING ←→ COMPLETED
    ↓
[Deleted]
```

**Invariants**:
- Every task MUST have a unique ID
- Every task MUST have a non-empty title
- Task IDs MUST never change after creation
- Deleted tasks are removed completely (no soft delete)

## TaskStatus Enum

**Purpose**: Represents the completion state of a task

**Values**:
- `PENDING`: Task not yet completed (default state)
- `COMPLETED`: Task finished/done

**Display Representation**:
- PENDING: "[ ] Pending" or "[ ] Pend."
- COMPLETED: "[✓] Completed" or "[✓] Comp."

## TaskManager (Business Logic)

**Purpose**: Manages the collection of tasks and enforces business rules

**Responsibilities**:
- Maintain in-memory list of tasks
- Generate unique auto-incrementing IDs
- Enforce validation rules
- Provide CRUD operations

**State**:

| Attribute | Type        | Purpose                                    |
|-----------|-------------|--------------------------------------------|
| _tasks    | list[Task]  | In-memory storage of all active tasks      |
| _next_id  | int         | Counter for next task ID (starts at 1)     |

**Operations**:

### add_task(title: str, description: str = "") -> Task
- **Pre-conditions**: title must be non-empty after stripping whitespace
- **Post-conditions**:
  - New task added to _tasks list
  - _next_id incremented by 1
  - Task has unique ID and status PENDING
- **Raises**: ValueError if title is empty/whitespace-only
- **Maps to**: FR-001, FR-002, FR-003, FR-004

### get_all_tasks() -> list[Task]
- **Pre-conditions**: None
- **Post-conditions**: Returns copy of all tasks (empty list if no tasks)
- **Raises**: Nothing
- **Maps to**: FR-005, FR-007

### get_task_by_id(task_id: int) -> Task | None
- **Pre-conditions**: task_id is valid integer
- **Post-conditions**: Returns task if found, None otherwise
- **Raises**: Nothing
- **Maps to**: FR-015

### update_task(task_id: int, title: str | None, description: str | None) -> Task
- **Pre-conditions**:
  - task_id exists in _tasks
  - If title provided, must be non-empty after stripping
- **Post-conditions**: Task updated with new title and/or description
- **Raises**:
  - ValueError if task not found
  - ValueError if title is empty/whitespace-only
- **Maps to**: FR-008, FR-009, FR-010, FR-015

### delete_task(task_id: int) -> bool
- **Pre-conditions**: None (gracefully handles non-existent IDs)
- **Post-conditions**:
  - Task removed from _tasks if found
  - _next_id unchanged (no ID reuse)
- **Raises**: ValueError if task not found
- **Maps to**: FR-011, FR-015, FR-019

### toggle_task_status(task_id: int) -> Task
- **Pre-conditions**: task_id exists in _tasks
- **Post-conditions**:
  - Task status toggled (PENDING ↔ COMPLETED)
  - Returns updated task
- **Raises**: ValueError if task not found
- **Maps to**: FR-013, FR-014, FR-015

## Data Flow

### Add Task Flow
```
User Input → Validate Title → Create Task with auto-ID → Add to _tasks → Return Task
```

### List Tasks Flow
```
User Request → Get all _tasks → Format for display → Show to user
```

### Update Task Flow
```
User Input (ID + new data) → Find task by ID → Validate new title → Update task → Return Task
```

### Delete Task Flow
```
User Input (ID) → Find task by ID → Remove from _tasks → Confirm deletion
```

### Toggle Status Flow
```
User Input (ID) → Find task by ID → Toggle status → Return Task
```

## Persistence Model

**Strategy**: In-memory only (FR-017)

**Lifecycle**:
1. Application starts: _tasks is empty list, _next_id = 1
2. During session: All changes kept in memory
3. Application exits: All data lost

**No Persistence**:
- No file I/O
- No database
- No serialization
- Data lost when process terminates (by design)

## Error Handling Strategy

**Validation Errors**:
- Empty title: `ValueError("Title cannot be empty")`
- Whitespace-only title: `ValueError("Title cannot be empty")`
- Invalid task ID format: `ValueError("Invalid task ID format: '<input>'")`
- Task not found: `ValueError("Task with ID <id> not found")`

**Display Format**:
All errors displayed to user as clear, actionable messages with suggestions.

## Display Constraints

**From FR-006**: Long descriptions truncated to ~50 characters with "..." indicator

**Truncation Rules**:
- Applied only at display layer (not in model)
- Preserve full text in Task object
- Truncate at word boundary when possible
- Add "..." suffix when truncated

**Example**:
```
Full description: "This is a very long description that exceeds fifty characters easily"
Display: "This is a very long description that exceeds..."
```

## Constraints Summary

| Constraint | Rule                                           | Source     |
|------------|------------------------------------------------|------------|
| ID Unique  | No two tasks can have same ID                  | FR-003     |
| ID Stable  | IDs never change, never reused                 | FR-019     |
| Title Req  | Title cannot be empty/whitespace               | FR-001     |
| Desc Opt   | Description can be empty                       | FR-002     |
| No Persist | Data lost on exit                              | FR-017     |
| Status Def | New tasks default to PENDING                   | FR-004     |
| Max Tasks  | Must handle 100+ tasks without degradation     | SC-004     |
