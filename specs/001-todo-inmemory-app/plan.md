# Implementation Plan: Todo In-Memory Console App

**Branch**: `001-todo-inmemory-app` | **Date**: 2025-12-29 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-todo-inmemory-app/spec.md`

## Summary

Build a command-line Todo application that stores tasks in memory only, providing 5 core features: Add Task, View/List Tasks, Update Task, Delete Task, and Mark Complete/Incomplete. Application uses Python 3.13+ with standard library only, implements clean architecture with separation of concerns, and provides intuitive REPL-based interface with comprehensive input validation.

**Key Technical Decisions** (from [research.md](research.md)):
- Command-based REPL interface using built-in `input()` function
- In-memory storage using Python list of dataclass Task objects
- Simple auto-incrementing integer IDs (never reused after deletion)
- Fixed-width ASCII table formatting for task display
- Validation at command handler level with clear error messages

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (Python standard library only)
**Storage**: In-memory list (no persistence, data lost on exit)
**Testing**: pytest or unittest (optional for development)
**Target Platform**: Cross-platform (Linux, macOS, Windows)
**Project Type**: Single console application
**Performance Goals**: Handle 100+ tasks, all operations < 1 second response time
**Constraints**: No external dependencies, no file I/O, PEP 8 compliance, type hints required
**Scale/Scope**: Small single-user application, ~500-800 lines of code estimated

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Note**: This project does not have a populated constitution file. The template constitution file contains only placeholders. Therefore, no constitution-based gates are enforced. The following default principles apply:

### Default Principles Applied

1. **Simplicity First**:
   - ✅ Single project structure (no unnecessary complexity)
   - ✅ No external dependencies (uses standard library only)
   - ✅ Clear separation of concerns (models, manager, commands, display, validation)

2. **Type Safety**:
   - ✅ Type hints required for all functions
   - ✅ Dataclasses for structured data (Task entity)
   - ✅ Enums for constrained values (TaskStatus)

3. **Input Validation**:
   - ✅ Validate all user inputs at entry points
   - ✅ Clear error messages for invalid inputs
   - ✅ Prevent crashes from malformed data

4. **Testing**:
   - ✅ Unit tests for all business logic components
   - ✅ Test coverage for edge cases listed in specification
   - ✅ Acceptance scenario testing

5. **Code Quality**:
   - ✅ PEP 8 compliance
   - ✅ Clear, descriptive naming
   - ✅ Docstrings for public APIs
   - ✅ No dead code or unused imports

**Constitution Status**: ✅ PASSED (using default principles, no violations)

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-inmemory-app/
├── spec.md                # Feature specification (COMPLETED)
├── plan.md                # This file (COMPLETED by /sp.plan)
├── research.md            # Technical decisions (COMPLETED by /sp.plan)
├── data-model.md          # Entity definitions (COMPLETED by /sp.plan)
├── quickstart.md          # Setup and usage guide (COMPLETED by /sp.plan)
├── contracts/             # Interface contracts (COMPLETED by /sp.plan)
│   └── cli-commands.md    # CLI command specifications
├── checklists/            # Quality gates
│   └── requirements.md    # Spec quality checklist (COMPLETED)
└── tasks.md               # Implementation tasks (NOT created yet - use /sp.tasks)
```

### Source Code (repository root)

```text
todo/
├── src/
│   ├── __init__.py         # Package marker
│   ├── main.py             # Entry point, CLI REPL loop
│   ├── models.py           # Task dataclass, TaskStatus enum
│   ├── task_manager.py     # TaskManager business logic class
│   ├── commands.py         # Command handler functions
│   ├── display.py          # Output formatting utilities
│   └── validation.py       # Input validation utilities
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py      # Task and TaskStatus tests
│   ├── test_task_manager.py # TaskManager CRUD operations tests
│   ├── test_commands.py    # Command handler tests
│   ├── test_validation.py  # Validation function tests
│   └── test_integration.py # End-to-end acceptance scenario tests
│
├── specs/                  # Feature specifications (this directory)
├── history/                # PHR records
├── .specify/               # SpecKit Plus configuration
├── README.md               # User-facing documentation
├── CLAUDE.md               # AI development log (to be created)
├── pyproject.toml          # UV project configuration
└── .gitignore              # Git ignore patterns
```

**Structure Decision**: Single project structure selected because:
- Application is self-contained (no separate frontend/backend/mobile)
- Clear module separation enables testing and maintenance
- Follows Python packaging best practices
- Aligns with "simplicity first" principle

## Implementation Phases

### Phase 0: Research & Technical Decisions ✅ COMPLETED

**Status**: All research completed and documented in [research.md](research.md)

**Completed Research**:
- ✅ Python 3.13+ standard library capabilities confirmed
- ✅ Command-line interface pattern selected (REPL with text parsing)
- ✅ Data structure for in-memory storage decided (list of Task dataclasses)
- ✅ ID generation strategy defined (simple counter, never reused)
- ✅ Input validation strategy established (validate at handler level)
- ✅ Display formatting approach chosen (ASCII table with manual truncation)
- ✅ Project structure defined (single project with clear separation)
- ✅ Testing strategy outlined (unit tests, no mocking for in-memory components)
- ✅ Performance considerations analyzed (no optimization needed for 100 tasks)
- ✅ User experience enhancements specified (clear indicators, helpful messages)

**Key Outputs**:
- [research.md](research.md) - All technical decisions documented
- [data-model.md](data-model.md) - Entity and business logic definitions
- [contracts/cli-commands.md](contracts/cli-commands.md) - CLI interface contracts
- [quickstart.md](quickstart.md) - Setup and usage documentation

### Phase 1: Data Model & Contracts ✅ COMPLETED

**Status**: All design artifacts completed

**Completed Deliverables**:
- ✅ [data-model.md](data-model.md) - Task entity, TaskStatus enum, TaskManager operations
- ✅ [contracts/cli-commands.md](contracts/cli-commands.md) - All 7 CLI commands specified
- ✅ [quickstart.md](quickstart.md) - User guide with examples

**Entity Summary**:
- **Task**: id (int), title (str), description (str), status (TaskStatus)
- **TaskStatus**: Enum with PENDING and COMPLETED states
- **TaskManager**: Business logic for CRUD operations with validation

**Contract Summary**:
- 7 commands: add, list, update, delete, complete, help, exit
- Error handling for all edge cases
- Performance target: all operations < 1 second

### Phase 2: Task Breakdown ⏸️ PENDING

**Status**: NOT STARTED - Use `/sp.tasks` command to generate

**What to expect from /sp.tasks**:
- Breakdown of implementation into small, testable tasks
- Dependency ordering (what must be built first)
- Test cases for each task (Red-Green-Refactor workflow)
- Acceptance criteria mapping to specification requirements

**Recommended task grouping** (preliminary, will be refined by /sp.tasks):
1. Project setup (UV, directory structure, pyproject.toml)
2. Core data model (Task, TaskStatus, validation functions)
3. TaskManager class (CRUD operations)
4. Display utilities (table formatting, truncation)
5. Command handlers (one task per command)
6. Main CLI loop (REPL, command parsing)
7. Integration testing (acceptance scenarios)
8. Documentation (README, CLAUDE.md)

## Complexity Tracking

**No Constitution Violations**: This section is not applicable because:
- Constitution file contains only template placeholders
- No specific project-level constraints are defined
- All design decisions follow standard best practices
- No unjustified complexity introduced

If constitution is populated in the future, this section will track any necessary violations with justifications.

## Architecture Overview

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         User                                │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                      main.py (CLI REPL)                     │
│  - Welcome message                                          │
│  - Command loop (input → parse → execute → output)          │
│  - Exit handling                                            │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                   commands.py (Handlers)                    │
│  - handle_add()      - handle_list()                        │
│  - handle_update()   - handle_delete()                      │
│  - handle_complete() - handle_help()                        │
└──────────┬──────────────────┬───────────────────┬───────────┘
           │                  │                   │
           ↓                  ↓                   ↓
┌──────────────────┐ ┌────────────────┐ ┌────────────────────┐
│  validation.py   │ │ display.py     │ │ task_manager.py    │
│                  │ │                │ │                    │
│ - validate_title │ │ - format_table │ │ - add_task()       │
│ - validate_id    │ │ - truncate()   │ │ - get_all_tasks()  │
│                  │ │ - show_error() │ │ - get_task_by_id() │
│                  │ │                │ │ - update_task()    │
│                  │ │                │ │ - delete_task()    │
│                  │ │                │ │ - toggle_status()  │
└──────────────────┘ └────────────────┘ └─────────┬──────────┘
                                                   │
                                                   ↓
                                        ┌──────────────────────┐
                                        │    models.py         │
                                        │                      │
                                        │ - Task (dataclass)   │
                                        │ - TaskStatus (enum)  │
                                        └──────────────────────┘
```

### Data Flow Examples

**Add Task Flow**:
```
User → main.py → handle_add() → validate_title() → task_manager.add_task() → Task created → display success
```

**List Tasks Flow**:
```
User → main.py → handle_list() → task_manager.get_all_tasks() → format_table() → display output
```

**Update Task Flow**:
```
User → main.py → handle_update() → validate_id() → validate_title() → task_manager.update_task() → display success
```

## Risk Assessment & Mitigation

### Low Risk ✅
- **Technology maturity**: Python 3.13 is stable and well-documented
- **Dependency management**: No external dependencies eliminates integration risks
- **Storage complexity**: In-memory storage is simple and reliable
- **Scope clarity**: All 20 functional requirements are clear and testable

### Medium Risk ⚠️
None identified

### High Risk 🔴
None identified

### Mitigation Strategies

1. **Input Validation**: Comprehensive validation prevents crashes (FR-020)
2. **Type Safety**: Type hints catch errors during development
3. **Testing**: Unit tests for all edge cases ensure robustness
4. **Clear Contracts**: Well-defined command contracts prevent ambiguity

## Success Criteria Mapping

Each success criterion from spec.md maps to implementation components:

| Criterion | Implementation Component | Verification Method |
|-----------|--------------------------|---------------------|
| SC-001: Add task < 10 seconds | handle_add() with efficient prompts | Manual timing test |
| SC-002: View list clearly | format_table() with fixed-width columns | Visual inspection |
| SC-003: All 5 operations work | All command handlers implemented | Integration tests |
| SC-004: Handle 100+ tasks | List-based storage, O(n) operations | Performance test with 100 tasks |
| SC-005: Clear error messages | Validation functions, error formatting | Error case testing |
| SC-006: Stable task IDs | Never decrement _next_id counter | Delete and re-add test |
| SC-007: Instant status ID | Visual indicators [ ] and [✓] | Visual inspection |
| SC-008: Feedback < 1 second | All operations in-memory, no I/O | Response time testing |
| SC-009: Handle edge cases | Validation for all listed edge cases | Edge case test suite |
| SC-010: Full lifecycle < 2 min | Efficient command processing | End-to-end manual test |

## Dependencies

### External Dependencies
**None** - Application uses Python standard library only

### Internal Module Dependencies

```
main.py
├── depends on: commands.py
└── depends on: display.py

commands.py
├── depends on: task_manager.py
├── depends on: validation.py
└── depends on: display.py

task_manager.py
└── depends on: models.py

display.py
└── depends on: models.py

validation.py
└── depends on: models.py

models.py
└── no dependencies (uses only standard library)
```

**Build Order** (bottom-up):
1. models.py (Task, TaskStatus)
2. validation.py
3. task_manager.py
4. display.py
5. commands.py
6. main.py

## Testing Strategy

### Test Levels

1. **Unit Tests** (test individual components):
   - test_models.py: Task dataclass, TaskStatus enum
   - test_validation.py: validate_title(), validate_task_id()
   - test_task_manager.py: All CRUD operations
   - test_display.py: Table formatting, truncation
   - test_commands.py: Each command handler

2. **Integration Tests** (test component interactions):
   - test_integration.py: Full command execution flows
   - Acceptance scenarios from spec.md

3. **Manual Tests** (user acceptance):
   - Complete task lifecycle (add → view → update → complete → delete)
   - All edge cases from specification
   - Performance with 100 tasks

### Test Coverage Goals

- **Minimum**: 80% code coverage
- **Target**: 90% code coverage
- **Critical paths**: 100% coverage (validation, CRUD operations)

### Test-Driven Development Workflow

Following Red-Green-Refactor cycle:

1. **Red**: Write failing test for requirement
2. **Green**: Implement minimum code to pass test
3. **Refactor**: Clean up code while keeping tests green

## Performance Targets

Based on SC-004 and SC-008:

| Operation | Max Response Time | Expected (100 tasks) |
|-----------|------------------|----------------------|
| Add task  | 1 second         | < 100ms              |
| List tasks| 1 second         | < 100ms              |
| Update task| 1 second        | < 100ms              |
| Delete task| 1 second        | < 100ms              |
| Complete task| 1 second      | < 100ms              |
| Help      | 1 second         | < 50ms               |
| Exit      | 1 second         | < 50ms               |

**Measurement**: Use Python's `time.perf_counter()` for performance testing

## Next Steps

1. **Run `/sp.tasks`** to generate detailed task breakdown
2. **Review tasks** and adjust if needed with `/sp.clarify`
3. **Begin implementation** following Red-Green-Refactor workflow
4. **Track progress** with task completion
5. **Create ADRs** for any significant architectural decisions (use `/sp.adr` if needed)
6. **Update CLAUDE.md** with all prompts and iterations

## Appendix: Functional Requirements Mapping

All 20 functional requirements from spec.md map to implementation components:

| FR-ID   | Requirement Summary | Implementation Component(s) |
|---------|---------------------|----------------------------|
| FR-001  | Add task with title | handle_add(), validate_title() |
| FR-002  | Optional description| handle_add(), Task.description |
| FR-003  | Auto-increment ID   | TaskManager._next_id |
| FR-004  | Default status PENDING | Task dataclass default |
| FR-005  | Display tasks in table | format_table(), handle_list() |
| FR-006  | Truncate long descriptions | truncate() in display.py |
| FR-007  | Empty state message | handle_list() with conditional |
| FR-008  | Update title by ID  | handle_update(), task_manager.update_task() |
| FR-009  | Update description  | handle_update(), task_manager.update_task() |
| FR-010  | Validate updated title | validate_title() |
| FR-011  | Delete task by ID   | handle_delete(), task_manager.delete_task() |
| FR-012  | Delete confirmation | handle_delete() success message |
| FR-013  | Toggle status       | handle_complete(), task_manager.toggle_status() |
| FR-014  | Status feedback     | handle_complete() with status display |
| FR-015  | Validate task IDs   | validate_task_id() |
| FR-016  | Handle invalid commands | main.py command parsing |
| FR-017  | In-memory only      | TaskManager._tasks (list, no file I/O) |
| FR-018  | CLI interface       | main.py REPL loop |
| FR-019  | Stable task IDs     | Never decrement _next_id |
| FR-020  | Prevent crashes     | All validation functions |

## Document Status

- ✅ **Phase 0 (Research)**: COMPLETED
- ✅ **Phase 1 (Design & Contracts)**: COMPLETED
- ⏸️ **Phase 2 (Task Breakdown)**: Use `/sp.tasks` command
- ⏸️ **Implementation**: Blocked until tasks generated
- ⏸️ **Testing**: Blocked until implementation

**Last Updated**: 2025-12-29 by Claude Code (/sp.plan command)
