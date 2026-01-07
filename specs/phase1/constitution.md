# Phase I Constitution - Todo In-Memory Console App

## Core Principles

### I. Simplicity First

Application MUST remain simple and focused. Use Python standard library only with no external dependencies. Single project structure with clear module separation. No unnecessary abstractions or premature optimization. Follow YAGNI (You Aren't Gonna Need It) principle.

**Rationale**: Simplicity reduces complexity, eliminates dependency management overhead, and makes the codebase easier to understand and maintain.

### II. Type Safety

All code MUST be fully typed with Python type hints on all public functions. Use dataclasses for structured data (Task entity) and Enums for constrained values (TaskStatus). Type safety is enforced at development time.

**Rationale**: Type hints catch errors during development, improve code documentation, and enable better IDE support and refactoring.

### III. Test-Driven Development (TDD)

Development MUST follow Red-Green-Refactor workflow:
1. **Red**: Write failing test for requirement
2. **Green**: Implement minimum code to pass test
3. **Refactor**: Clean up code while keeping tests green

All business logic must have unit test coverage. All edge cases must be tested.

**Rationale**: TDD ensures requirements are testable, catches regressions early, and produces well-designed, maintainable code.

### IV. Input Validation and Error Handling

All user inputs MUST be validated at command handler level. Invalid inputs must result in clear, actionable error messages—never crashes. Validate early, fail gracefully, and provide helpful feedback.

**Rationale**: Robust input validation prevents crashes, improves user experience, and ensures application stability.

### V. In-Memory Storage Only

All task data MUST be stored in memory only using Python lists. No file I/O, no databases, no persistence. Data is lost when application exits. This is an intentional constraint.

**Rationale**: In-memory storage keeps Phase I simple and fast. Persistence is explicitly deferred to Phase II to focus on core functionality first.

### VI. Command-Line Interface (CLI)

Application MUST provide a REPL (Read-Eval-Print-Loop) command-line interface. All interactions happen via text commands. Commands must be intuitive, consistent, and well-documented with a help command.

**Rationale**: CLI interface is simple to implement, easy to test, and provides immediate user feedback without UI complexity.

### VII. Clean Architecture and Separation of Concerns

Codebase MUST maintain clear module boundaries:
- **models.py**: Data structures (Task, TaskStatus)
- **task_manager.py**: Business logic (CRUD operations)
- **commands.py**: Command handlers (user interface layer)
- **display.py**: Output formatting
- **validation.py**: Input sanitization
- **main.py**: Entry point and REPL loop

No layer may directly access another layer's internals. Dependencies flow in one direction (main → commands → task_manager → models).

**Rationale**: Separation of concerns enables independent testing, easier maintenance, and clearer reasoning about code behavior.

## Code Quality Standards

### Python Requirements
- **Version**: Python 3.13 or higher
- **Style**: PEP 8 compliant
- **Type Hints**: Required on all public functions
- **Docstrings**: Required for all public classes and functions
- **No Dead Code**: Remove unused imports and functions

### Testing Requirements
- **Unit Tests**: Core business logic must have unit test coverage
- **Edge Case Tests**: All edge cases from specification must be tested
- **Integration Tests**: Acceptance scenarios from spec must be verified
- **Minimum Coverage**: 80% code coverage
- **Target Coverage**: 90% code coverage
- **Critical Path Coverage**: 100% (validation, CRUD operations)

### Performance Standards
- **Response Time**: All operations must complete in < 1 second
- **Scale**: Must handle 100+ tasks without degradation
- **Memory**: Efficient list operations (O(n) acceptable for this scale)

## Project Structure

### Directory Layout
```
/
├── src/                   # Source code
│   ├── __init__.py
│   ├── main.py            # Entry point and REPL
│   ├── models.py          # Task dataclass, TaskStatus enum
│   ├── task_manager.py    # Business logic
│   ├── commands.py        # Command handlers
│   ├── display.py         # Output formatting
│   └── validation.py      # Input validation
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_task_manager.py
│   ├── test_commands.py
│   ├── test_validation.py
│   ├── test_display.py
│   └── test_integration.py
├── specs/                 # Feature specifications
│   └── 001-todo-inmemory-app/
├── README.md              # User documentation
└── pyproject.toml         # Project configuration
```

## Development Workflow

### 1. Specification Phase
- Define user stories with priorities (P1, P2, P3)
- List functional requirements (FR-001, FR-002, etc.)
- Define success criteria (measurable outcomes)
- Identify edge cases

### 2. Planning Phase
- Make technical decisions (documented in research.md)
- Define data model (documented in data-model.md)
- Specify contracts (documented in contracts/)
- Create quickstart guide

### 3. Task Breakdown
- Break features into small, testable tasks
- Order tasks by dependencies
- Include test cases for each task

### 4. Implementation (TDD)
- Write failing test first
- Implement minimum code to pass
- Refactor while keeping tests green
- Commit after each task or logical group

### 5. Validation
- Run all tests (must pass 100%)
- Manual testing of user flows
- Performance testing with 100 tasks
- Edge case verification

## Functional Requirements

Phase I implements 5 core features:

1. **Add Task**: Create task with title (required) and description (optional)
2. **View/List Tasks**: Display all tasks in formatted table
3. **Update Task**: Modify task title and/or description
4. **Delete Task**: Permanently remove task
5. **Mark Complete/Incomplete**: Toggle task status

### Task Entity
- **id**: Unique auto-incrementing integer (never reused)
- **title**: Non-empty string (required)
- **description**: String (optional, can be empty)
- **status**: TaskStatus enum (PENDING or COMPLETED)

### CLI Commands
- `add` - Add a new task
- `list` - View all tasks
- `update` - Update a task
- `delete` - Delete a task
- `mark` or `complete` - Toggle task status
- `help` - Show available commands
- `exit` or `quit` - Exit application

## Constraints

### Non-Negotiable Constraints
- **No external dependencies**: Python standard library only
- **No persistence**: In-memory storage only (data lost on exit)
- **No file I/O**: No reading/writing files
- **Single user**: Designed for individual use
- **CLI only**: No GUI, no web interface

### Development Constraints
- **Type hints required**: All public functions must be typed
- **PEP 8 compliance**: Code style must follow PEP 8
- **Test coverage**: Minimum 80% coverage required
- **Small commits**: Commit after each task or logical group

## Success Criteria

Phase I is successful when:

- ✅ All 5 core features are functional
- ✅ All 20 functional requirements (FR-001 to FR-020) are met
- ✅ All acceptance scenarios pass
- ✅ All edge cases are handled gracefully
- ✅ Application handles 100+ tasks without degradation
- ✅ All operations complete in < 1 second
- ✅ Test coverage >= 80%
- ✅ Zero crashes from invalid input
- ✅ Task IDs remain stable (never reused)
- ✅ User can complete full task lifecycle in < 2 minutes

## Governance

### Constitution Authority
This Phase I constitution defines the principles and constraints for the in-memory console application. It supersedes general development practices when conflicts arise.

### Phase Transition
When transitioning to Phase II (full-stack web app):
- Phase I code is preserved but moved to `/console` directory
- Phase II introduces new constitution with different principles (persistence, multi-user, web API)
- Phase I constitution remains authoritative for console app maintenance

### Amendment Process
Amendments to Phase I constitution require:
1. Documented justification for the change
2. User approval
3. Version increment (semantic versioning)
4. Update to dependent documentation

### Compliance
- All code must comply with these principles
- Test coverage requirements are enforced
- Type hints are mandatory and checked
- PEP 8 compliance verified with linters

**Version**: 1.0.0 | **Ratified**: 2025-12-29 | **Last Amended**: 2026-01-02
