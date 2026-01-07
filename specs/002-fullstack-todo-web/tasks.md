# Task Breakdown: Multi-User Full-Stack Todo Web Application

**Branch**: `002-fullstack-todo-web`
**Date**: 2026-01-02
**Plan Reference**: [plan.md](./plan.md)
**Spec Reference**: [spec.md](./spec.md)
**Status**: Ready for Execution

This task breakdown follows the approved Implementation Plan and Specification. All tasks are small, independent, testable, and ordered by dependencies. Follow strict Red-Green-Refactor workflow using Claude Code only.

## Phase 1: Monorepo Setup & Foundation
- [x] T001 Move existing Phase I code to /console/ directory
- [x] T002 Create /frontend/ with Next.js 16+ App Router project (TypeScript, Tailwind)
- [x] T003 Create /backend/ with FastAPI project structure
- [x] T004 Add .env.example files for both frontend and backend (include BETTER_AUTH_SECRET, DATABASE_URL)
- [x] T005 Generate shared BETTER_AUTH_SECRET and document in both .env.example
- [x] T006 Add .gitignore rules for .env* files
- [x] T007 Complete CHECKPOINT 1: Both apps start without errors (npm run dev & uvicorn main:app)

## Phase 2: Authentication & Security Foundation
- [x] T008 [P] Configure Better Auth in frontend with JWT plugin enabled
- [x] T009 [P] Implement signup and signin pages in frontend (/signup, /signin)
- [x] T010 [P] Implement JWT verification dependency in backend (extract user_id from token)
- [x] T011 [P] Add CORS middleware in FastAPI (allow localhost:3000 with credentials)
- [x] T012 [P] Test auth flow: signup → JWT issued → backend validates token
- [x] T013 Complete CHECKPOINT 2: User can sign up/sign in, backend protected route returns user_id

## Phase 3: Database Schema & Models
- [x] T014 Create database.py with async engine and session dependency
- [x] T015 Define SQLModel Task model (id, user_id, title, description, completed, timestamps)
- [x] T016 Implement init_db script to create tables and indexes
- [x] T017 Test database connection and schema creation
- [x] T018 Complete CHECKPOINT 3: tasks table exists with correct schema and indexes (SQLite for dev)

## Phase 4: Backend API Implementation
- [x] T019 Create Pydantic models for TaskCreate, TaskUpdate, TaskResponse
- [x] T020 Implement GET /api/tasks (list user's tasks)
- [x] T021 Implement POST /api/tasks (create task for user)
- [x] T022 Implement GET /api/tasks/{id} (single task with ownership check)
- [x] T023 Implement PUT /api/tasks/{id} (update with ownership)
- [x] T024 Implement PATCH /api/tasks/{id}/toggle (toggle completion)
- [x] T025 Implement DELETE /api/tasks/{id} (delete with ownership)
- [x] T026 Add proper error handling (401, 404 indistinguishable, 400 validation)
- [x] T027 Complete CHECKPOINT 4: All 6 endpoints work with JWT, enforce user isolation

## Phase 5: Frontend Task UI & Integration
- [x] T028 Implement middleware for protected routes (redirect to signin if no token)
- [x] T029 Create tasks page (server component fetching tasks)
- [x] T030 Implement TaskList component (client) with status indicators and truncation
- [x] T031 Implement TaskForm component for add/edit
- [x] T032 Implement toggle, delete, and edit actions with API calls
- [x] T033 Add empty state and responsive Tailwind styling
- [x] T034 Handle token expiration (redirect to signin, preserve work)
- [x] T035 Complete CHECKPOINT 5: Full task lifecycle works for authenticated user

## Phase 6: Polish & User Experience
- [x] T036 [P] Add loading states and spinners
- [x] T037 [P] Implement optimistic updates for create/toggle/delete
- [x] T038 [P] Add success/error toast notifications (react-hot-toast)
- [x] T039 [P] Implement logout functionality (Header component)
- [x] T040 [P] Improve accessibility (ARIA, keyboard navigation)
- [x] T041 Complete CHECKPOINT 6: Smooth, responsive UX with feedback

## Phase 7: Testing & Validation
- [x] T042 [P] Write backend unit tests for models and JWT validation
- [x] T043 [P] Write backend integration tests for all endpoints
- [x] T044 [P] Test multi-user isolation (two users, no data leakage)
- [x] T045 [P] Write frontend component tests
- [x] T046 [P] Manual E2E test: full user journey and edge cases
- [x] T047 Complete CHECKPOINT 7: All tests pass, isolation verified

## Phase 8: Final Deliverables & Documentation
- [x] T048 Complete README.md with setup and run instructions
- [x] T049 Update quickstart.md and add deployment notes
- [x] T050 Finalize CLAUDE.md with prompt history
- [x] T051 Organize specs/phase2/ with all files
- [x] T052 Final code cleanup (linters, remove debug logs)
- [x] T053 Complete CHECKPOINT 8: Repository complete, ready for submission/demo

## Success Gate
Project complete when:
- All checkpoints passed sequentially
- All acceptance criteria from spec.md met
- Multi-user isolation fully enforced
- Data persists in PostgreSQL
- Clean, professional monorepo with all deliverables

**Execution Order**: Follow phases strictly. Complete checkpoint before next phase.

**Next Action**: Start with Task 1.1. Generate and place all files exactly as specified.