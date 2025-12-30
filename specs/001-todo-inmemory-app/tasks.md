# Tasks: Todo In-Memory Console App

**Input**: Design documents from `/specs/001-todo-inmemory-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-commands.md

**Tests**: This feature includes comprehensive test tasks following TDD (Red-Green-Refactor) workflow as specified in the implementation plan.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow single project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create directory structure with src/, tests/, specs/, history/, .specify/ directories
- [x] T002 Initialize pyproject.toml for Python 3.13+ with uv (no external dependencies)
- [x] T003 [P] Create src/__init__.py package marker
- [x] T004 [P] Create tests/__init__.py package marker
- [x] T005 [P] Create .gitignore with Python patterns (__pycache__, *.pyc, .env, etc.)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 [P] Implement TaskStatus enum (PENDING, COMPLETED) in src/models.py
- [x] T007 [P] Implement Task dataclass with id, title, description, status fields in src/models.py
- [x] T008 [P] Add type hints and defaults (status=TaskStatus.PENDING, description="") to Task in src/models.py
- [x] T009 [P] Implement validate_title(title: str) function in src/validation.py
- [x] T010 [P] Implement validate_task_id(task_id: str, tasks: list[Task]) function in src/validation.py
- [x] T011 Implement TaskManager class with _tasks list and _next_id counter in src/task_manager.py
- [x] T012 [P] Implement truncate(text: str, max_length: int) function in src/display.py
- [x] T013 [P] Implement format_task_row(task: Task) function in src/display.py
- [x] T014 [P] Implement format_task_table(tasks: list[Task]) function in src/display.py
- [x] T015 [P] Implement show_empty_message() and message helpers in src/display.py
- [x] T016 Create basic main.py REPL structure with welcome message and input loop
- [x] T017 Add exit/quit command handling to main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add new tasks and view all tasks in a clean table format

**Independent Test**: Add one or more tasks and list them. Delivers immediate value by allowing users to externalize thoughts into a task list.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T018 [P] [US1] Write unit tests for Task dataclass creation in tests/test_models.py
- [x] T019 [P] [US1] Write unit tests for TaskStatus enum in tests/test_models.py
- [x] T020 [P] [US1] Write unit tests for validate_title() with valid/invalid inputs in tests/test_validation.py
- [x] T021 [P] [US1] Write unit tests for TaskManager.add_task() in tests/test_task_manager.py
- [x] T022 [P] [US1] Write unit tests for TaskManager.get_all_tasks() in tests/test_task_manager.py
- [x] T023 [P] [US1] Write unit tests for display formatting functions in tests/test_display.py
- [x] T024 [P] [US1] Write integration test for add command flow in tests/test_integration.py
- [x] T025 [P] [US1] Write integration test for list command flow in tests/test_integration.py

### Implementation for User Story 1

- [x] T026 [US1] Implement TaskManager.add_task(title, description) method in src/task_manager.py
- [x] T027 [US1] Implement TaskManager.get_all_tasks() method in src/task_manager.py
- [x] T028 [US1] Implement handle_add(manager) command handler in src/commands.py
- [x] T029 [US1] Implement handle_list(manager) command handler in src/commands.py
- [x] T030 [US1] Implement handle_help() command handler in src/commands.py
- [x] T031 [US1] Wire add and list commands to main.py REPL loop
- [x] T032 [US1] Add error handling for empty titles in handle_add
- [x] T033 [US1] Add empty state message handling in handle_list

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently
- ✓ Can add tasks with title (required) and description (optional)
- ✓ Can view all tasks in formatted table
- ✓ Empty list shows helpful message
- ✓ Invalid inputs show clear error messages

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Users can toggle task status between Pending and Completed to track progress

**Independent Test**: Add tasks, mark them complete, verify status changes are reflected in the task list

### Tests for User Story 2

- [x] T034 [P] [US2] Write unit tests for TaskManager.get_task_by_id() in tests/test_task_manager.py
- [x] T035 [P] [US2] Write unit tests for TaskManager.toggle_status() in tests/test_task_manager.py
- [x] T036 [P] [US2] Write unit tests for validate_task_id() in tests/test_validation.py
- [x] T037 [P] [US2] Write integration test for complete command flow in tests/test_integration.py

### Implementation for User Story 2

- [x] T038 [US2] Implement TaskManager.get_task_by_id(id) method in src/task_manager.py
- [x] T039 [US2] Implement TaskManager.toggle_status(id) method in src/task_manager.py
- [x] T040 [US2] Implement handle_mark(manager) command handler in src/commands.py
- [x] T041 [US2] Wire mark command to main.py REPL loop
- [x] T042 [US2] Add error handling for invalid task IDs in handle_mark
- [x] T043 [US2] Add status feedback messages (showing new status) in handle_mark

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently
- ✓ Can mark tasks as completed or pending
- ✓ Status changes are visible in task list with clear indicators ([ ] and [✓])
- ✓ Invalid task IDs show clear error messages

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Users can modify task title and/or description for existing tasks

**Independent Test**: Create a task, update its title and/or description, verify changes are reflected

### Tests for User Story 3

- [x] T044 [P] [US3] Write unit tests for TaskManager.update_task() in tests/test_task_manager.py
- [x] T045 [P] [US3] Write integration test for update command flow in tests/test_integration.py
- [x] T046 [P] [US3] Write edge case tests for update with empty title in tests/test_integration.py

### Implementation for User Story 3

- [x] T047 [US3] Implement TaskManager.update_task(id, title, description) method in src/task_manager.py
- [x] T048 [US3] Implement handle_update(manager) command handler in src/commands.py
- [x] T049 [US3] Wire update command to main.py REPL loop
- [x] T050 [US3] Add validation for empty title in handle_update
- [x] T051 [US3] Add error handling for invalid task IDs in handle_update
- [x] T052 [US3] Add success confirmation messages in handle_update

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently
- ✓ Can update task title and/or description by ID
- ✓ Empty titles are rejected with clear error
- ✓ Invalid task IDs show clear error messages
- ✓ Success messages confirm updates

---

## Phase 6: User Story 4 - Delete Unwanted Tasks (Priority: P3)

**Goal**: Users can permanently remove tasks that are no longer relevant

**Independent Test**: Create tasks, delete specific ones, verify they no longer appear in the task list

### Tests for User Story 4

- [x] T053 [P] [US4] Write unit tests for TaskManager.delete_task() in tests/test_task_manager.py
- [x] T054 [P] [US4] Write integration test for delete command flow in tests/test_integration.py
- [x] T055 [P] [US4] Write test verifying ID stability (IDs not reused) in tests/test_task_manager.py

### Implementation for User Story 4

- [x] T056 [US4] Implement TaskManager.delete_task(id) method in src/task_manager.py
- [x] T057 [US4] Implement handle_delete(manager) command handler in src/commands.py
- [x] T058 [US4] Wire delete command to main.py REPL loop
- [x] T059 [US4] Add error handling for invalid task IDs in handle_delete
- [x] T060 [US4] Add success confirmation messages in handle_delete

**Checkpoint**: All user stories should now be independently functional
- ✓ Can delete tasks by ID
- ✓ Task IDs remain stable (no re-numbering after deletion)
- ✓ Invalid task IDs show clear error messages
- ✓ Success messages confirm deletion

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final quality checks

- [x] T061 [P] Implement parse_command(input) function for command routing in src/commands.py
- [x] T062 Add unknown command handling with helpful error in main.py
- [x] T063 [P] Add comprehensive docstrings to all public functions and classes
- [x] T064 [P] Ensure PEP 8 compliance across all src/ modules
- [x] T065 [P] Add type hints to all function signatures
- [x] T066 [P] Write edge case tests for very long titles/descriptions in tests/test_validation.py
- [x] T067 [P] Write edge case tests for whitespace-only titles in tests/test_validation.py
- [x] T068 [P] Write edge case tests for non-numeric task IDs in tests/test_validation.py
- [x] T069 Write performance test with 100+ tasks in tests/test_integration.py
- [x] T070 Write full task lifecycle integration test (add→view→update→complete→delete) in tests/test_integration.py
- [x] T071 Create comprehensive README.md with setup and usage instructions
- [x] T072 Create CLAUDE.md with full prompt history and development notes
- [x] T073 [P] Run all tests and verify 100% pass
- [x] T074 Manual acceptance test for all user stories from spec.md
- [x] T075 Validate all success criteria (SC-001 to SC-010) are met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (US1 → US2 → US3 → US4)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent but uses US1 infrastructure (TaskManager, display)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent but uses US1 infrastructure
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Independent but uses US1 infrastructure

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Core TaskManager methods before command handlers
- Command handlers before wiring to main.py
- Error handling after basic implementation
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (5 tasks)
- All Foundational tasks marked [P] can run in parallel (9 tasks: T006-T010, T012-T015)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
  - US1: 8 test tasks (T018-T025)
  - US2: 4 test tasks (T034-T037)
  - US3: 3 test tasks (T044-T046)
  - US4: 3 test tasks (T053-T055)
- Polish phase: many tasks marked [P] can run in parallel (10 tasks: T063-T068, T071-T073)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (Red phase - ensure they FAIL):
Task T018: "Write unit tests for Task dataclass creation in tests/test_models.py"
Task T019: "Write unit tests for TaskStatus enum in tests/test_models.py"
Task T020: "Write unit tests for validate_title() with valid/invalid inputs in tests/test_validation.py"
Task T021: "Write unit tests for TaskManager.add_task() in tests/test_task_manager.py"
Task T022: "Write unit tests for TaskManager.get_all_tasks() in tests/test_task_manager.py"
Task T023: "Write unit tests for display formatting functions in tests/test_display.py"
Task T024: "Write integration test for add command flow in tests/test_integration.py"
Task T025: "Write integration test for list command flow in tests/test_integration.py"

# After tests are written and failing, implement in sequence (Green phase):
# T026 → T027 → T028 → T029 → T030 → T031 → T032 → T033
```

---

## Parallel Example: Foundational Phase

```bash
# Launch all independent foundational tasks together:
Task T006: "Implement TaskStatus enum (PENDING, COMPLETED) in src/models.py"
Task T007: "Implement Task dataclass with id, title, description, status fields in src/models.py"
Task T008: "Add type hints and defaults (status=TaskStatus.PENDING, description='') to Task in src/models.py"
Task T009: "Implement validate_title(title: str) function in src/validation.py"
Task T010: "Implement validate_task_id(task_id: str, tasks: list[Task]) function in src/validation.py"
Task T012: "Implement truncate(text: str, max_length: int) function in src/display.py"
Task T013: "Implement format_task_row(task: Task) function in src/display.py"
Task T014: "Implement format_task_table(tasks: list[Task]) function in src/display.py"
Task T015: "Implement show_empty_message() and message helpers in src/display.py"

# Then complete sequential dependencies:
# T011 (TaskManager - depends on T006, T007)
# T016 (main.py - can be parallel with T011)
# T017 (exit handling - depends on T016)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005) - 5 tasks
2. Complete Phase 2: Foundational (T006-T017) - 12 tasks - CRITICAL
3. Complete Phase 3: User Story 1 (T018-T033) - 16 tasks
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready
6. **Total MVP tasks**: 33 tasks

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (17 tasks)
2. Add User Story 1 (16 tasks) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (10 tasks) → Test independently → Deploy/Demo
4. Add User Story 3 (9 tasks) → Test independently → Deploy/Demo
5. Add User Story 4 (8 tasks) → Test independently → Deploy/Demo
6. Polish (15 tasks) → Final validation and documentation
7. **Total tasks**: 75 tasks
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (17 tasks)
2. Once Foundational is done:
   - Developer A: User Story 1 (16 tasks)
   - Developer B: User Story 2 (10 tasks)
   - Developer C: User Story 3 (9 tasks)
   - Developer D: User Story 4 (8 tasks)
3. Stories complete and integrate independently
4. Team collaborates on Polish phase (15 tasks)

---

## Task Summary

**Total Tasks**: 75

### By Phase:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 12 tasks
- Phase 3 (US1 - Create and View): 16 tasks (8 tests + 8 implementation)
- Phase 4 (US2 - Mark Complete): 10 tasks (4 tests + 6 implementation)
- Phase 5 (US3 - Update Details): 9 tasks (3 tests + 6 implementation)
- Phase 6 (US4 - Delete Tasks): 8 tasks (3 tests + 5 implementation)
- Phase 7 (Polish): 15 tasks

### By Type:
- Setup/Infrastructure: 17 tasks (Phase 1 + Phase 2)
- Test tasks: 21 tasks (TDD approach)
- Implementation tasks: 37 tasks (including command handlers, business logic)

### Parallel Opportunities:
- Phase 1: 3 parallel tasks (T003, T004, T005)
- Phase 2: 9 parallel tasks (T006-T010, T012-T015)
- Phase 3 (US1): 8 parallel test tasks (T018-T025)
- Phase 4 (US2): 4 parallel test tasks (T034-T037)
- Phase 5 (US3): 3 parallel test tasks (T044-T046)
- Phase 6 (US4): 3 parallel test tasks (T053-T055)
- Phase 7: 10 parallel tasks (T063-T068, T071-T073)
- **Total parallelizable**: 40 tasks (53% of all tasks)

### Critical Path (MVP):
Setup (5) → Foundational (12) → US1 Tests (8) → US1 Implementation (8) = **33 tasks minimum for MVP**

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **TDD Workflow**: Write tests first (Red), implement to pass (Green), refactor
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Format Validation

✅ All 75 tasks follow the required checklist format:
- `- [ ]` checkbox prefix
- `[ID]` sequential task number (T001-T075)
- `[P]` marker for parallelizable tasks (40 tasks)
- `[Story]` label for user story tasks (US1, US2, US3, US4)
- Clear description with exact file paths
- No vague or underspecified tasks
