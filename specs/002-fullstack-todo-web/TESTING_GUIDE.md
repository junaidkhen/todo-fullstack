# Testing Guide

**Project**: Todo Fullstack Web App
**Date**: 2026-01-03
**Phase**: 7 - Testing & Validation

---

## Overview

This project has comprehensive test coverage across backend and frontend:
- **Backend**: pytest with async support for API integration tests
- **Frontend**: Jest + React Testing Library for component tests
- **E2E**: Manual test scenarios documented in E2E_TEST_SCENARIOS.md

---

## Backend Tests

### Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Activate virtual environment** (if using one):
   ```bash
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate   # Windows
   ```

3. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_models.py
pytest tests/integration/test_api.py

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

### Test Structure

```
backend/tests/
├── __init__.py
├── conftest.py                    # Shared fixtures
├── unit/
│   ├── test_models.py             # Model validation tests
│   └── test_jwt.py                # JWT authentication tests
└── integration/
    ├── test_api.py                # All 6 CRUD endpoint tests
    └── test_multi_user.py         # Multi-user isolation tests (CRITICAL)
```

### Coverage Summary

- **Unit Tests**:
  - Task and User model validation
  - JWT token creation and validation
  - Password hashing

- **Integration Tests**:
  - GET /api/tasks - List all tasks
  - POST /api/tasks - Create task
  - GET /api/tasks/{id} - Get single task
  - PATCH /api/tasks/{id} - Update task
  - PATCH /api/tasks/{id}/toggle - Toggle completion
  - DELETE /api/tasks/{id} - Delete task

- **Multi-User Tests** (Security Critical):
  - Users can only see their own tasks
  - Users cannot access other users' tasks by ID
  - Proper 404 responses prevent user enumeration
  - Concurrent operations are isolated

---

## Frontend Tests

### Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

### Running Tests

```bash
# Run all tests
npm test

# Run in watch mode (for development)
npm run test:watch

# Run with coverage report
npm run test:coverage

# Run specific test file
npm test TaskForm.test.tsx
```

### Test Structure

```
frontend/src/components/__tests__/
├── TaskForm.test.tsx              # Task creation form tests
├── TaskItem.test.tsx              # Individual task display/actions tests
├── TaskList.test.tsx              # Task list with CRUD operations tests
└── Header.test.tsx                # Header with logout tests
```

### Coverage Summary

**TaskForm Component**:
- Form rendering and validation
- Character counters (title: 200, description: 5000)
- Successful task creation
- Error handling (empty title, too long, API errors)
- Loading states
- Toast notifications
- Accessibility (ARIA labels)

**TaskItem Component**:
- Task display (title, description, status)
- Completion toggle
- Edit and delete actions
- Loading states
- Completed task styling (strike-through)
- Accessibility

**TaskList Component**:
- Empty state
- Task list rendering
- Task count summary
- Optimistic updates with rollback
- Toggle completion with toast feedback
- Delete with confirmation
- Error handling
- Preventing duplicate operations

**Header Component**:
- Logout functionality
- Loading states
- Error handling
- Token clearing
- Navigation to signin
- Multiple request prevention

---

## Manual E2E Tests

See [E2E_TEST_SCENARIOS.md](./E2E_TEST_SCENARIOS.md) for comprehensive manual testing checklist.

**8 Major Scenarios**:
1. New User Signup & First Task
2. Task Management (CRUD Operations)
3. Multi-User Isolation (Security)
4. Authentication & Session Management
5. UI/UX Polish & Accessibility
6. Edge Cases & Error Handling
7. Cross-Browser & Responsive Testing
8. Performance Testing

**Total**: ~100 manual test steps

---

## Continuous Integration

### GitHub Actions (Recommended)

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          npm run test:coverage
```

---

## Test Coverage Goals

| Component | Target | Current Status |
|-----------|--------|----------------|
| Backend Models | 90% | ✅ Achieved |
| Backend API | 90% | ✅ Achieved |
| Backend Auth | 100% | ✅ Achieved |
| Frontend Components | 70% | ✅ Achieved |
| Multi-User Isolation | 100% | ✅ Achieved |

---

## Critical Test Failures

If any of these tests fail, **DO NOT DEPLOY**:

1. ❌ `test_multi_user.py::test_user_cannot_access_other_user_task`
   - **Impact**: Security vulnerability - data leakage between users

2. ❌ `test_jwt.py::test_expired_token_rejected`
   - **Impact**: Security vulnerability - expired sessions accepted

3. ❌ `test_api.py::test_create_task_requires_auth`
   - **Impact**: Security vulnerability - unauthenticated access

4. ❌ `test_multi_user.py::test_user_cannot_delete_other_user_task`
   - **Impact**: Security vulnerability - unauthorized deletions

---

## Debugging Failed Tests

### Backend Test Failures

```bash
# Run single test with detailed output
pytest tests/integration/test_api.py::test_create_task -vv -s

# Drop into debugger on failure
pytest --pdb

# Show local variables on failure
pytest -l
```

### Frontend Test Failures

```bash
# Run single test with verbose output
npm test -- TaskForm.test.tsx --verbose

# Debug in watch mode
npm run test:watch -- TaskForm.test.tsx
```

### Common Issues

1. **Database not initialized**: Run `python init_db.py` in backend
2. **Missing dependencies**: Run `pip install -r requirements.txt` or `npm install`
3. **Port conflicts**: Ensure test server ports (8000, 3000) are available
4. **Auth token issues**: Check localStorage mocking in jest.setup.js

---

## Next Steps

After all tests pass:
1. ✅ Run backend tests: `cd backend && pytest`
2. ✅ Run frontend tests: `cd frontend && npm test`
3. ✅ Execute manual E2E scenarios from E2E_TEST_SCENARIOS.md
4. ✅ Fix any critical bugs found
5. ✅ Mark CHECKPOINT 7 as complete
6. 🚀 Proceed to Phase 8: Documentation & Deployment

---

**Test Status**: Phase 7 Complete
**Last Updated**: 2026-01-03
