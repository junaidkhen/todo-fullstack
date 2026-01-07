# Implementation Plan: Multi-User Full-Stack Todo Web Application

**Branch**: `002-fullstack-todo-web` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-fullstack-todo-web/spec.md`

## Summary

Transform Phase I console todo app into a production-ready multi-user web application with persistent PostgreSQL storage, Better Auth JWT authentication, Next.js 16+ frontend, and FastAPI async backend. System will implement all 5 core task features (create, view, update, complete, delete) with strict multi-user isolation, type safety, and RESTful API design.

**Key Evolution from Phase I**:
- Console CLI → Web UI (Next.js App Router with Tailwind CSS)
- In-memory storage → Persistent PostgreSQL (Neon serverless)
- No auth → Better Auth with JWT tokens
- Single user → Multi-user with data isolation
- Synchronous → Async architecture (FastAPI + asyncpg)

---

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.x with Next.js 16.0.10
- Backend: Python 3.13+

**Primary Dependencies**:
- Frontend: Next.js 16+, Better Auth (JWT plugin), Tailwind CSS 3.x, TypeScript strict mode
- Backend: FastAPI 0.115+, SQLModel 0.0.22+, PyJWT 2.x, asyncpg 0.30+

**Storage**: Neon PostgreSQL (serverless) with SQLModel ORM and async driver (asyncpg)

**Testing**:
- Frontend: Jest + React Testing Library
- Backend: pytest with async support
- Integration: Full-stack E2E tests

**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)

**Project Type**: Web application (monorepo: /console, /frontend, /backend)

**Performance Goals**:
- Task list load: <2 seconds for 100 tasks
- Task creation: <1 second
- User action feedback: <1 second
- Support 50 concurrent users

**Constraints**:
- No offline mode (requires internet connection)
- No real-time sync (optimized for single-device usage)
- Browser-based (no native mobile apps)
- Session-based auth (no OAuth/SSO in MVP)

**Scale/Scope**:
- Target: 50 concurrent users
- Per-user capacity: 1000 tasks
- Total system: ~50,000 tasks across all users

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Checked against: `specs/phase2/constitution.md` (v1.0.0)

### ✅ Passing Gates

| Principle | Status | Evidence |
|-----------|--------|----------|
| **I. Spec-Driven Development** | ✅ PASS | Specification created first (`spec.md`), clarified (`/sp.clarify`), and approved before implementation |
| **II. Multi-User Data Isolation** | ✅ PASS | Foreign key constraints (CASCADE DELETE), JWT-based user_id extraction, all queries filtered by user_id |
| **III. Clean Architecture** | ✅ PASS | Clear separation: Next.js (presentation) → FastAPI (business logic) → SQLModel (data access) → PostgreSQL (storage) |
| **IV. Stateless JWT Authentication** | ✅ PASS | Better Auth JWT tokens, shared `BETTER_AUTH_SECRET`, stateless validation on every request |
| **V. Type Safety** | ✅ PASS | TypeScript strict mode (frontend), Python type hints (backend), Pydantic validation (API contracts) |
| **VI. Persistent Storage with ORMs** | ✅ PASS | SQLModel ORM with PostgreSQL, async drivers, parameterized queries, no raw SQL |
| **VII. RESTful API Design** | ✅ PASS | Standard HTTP verbs (GET/POST/PUT/PATCH/DELETE), `/api/tasks` resource, proper status codes |

### Constitution Compliance Summary

**Result**: ✅ **ALL GATES PASSED** - No violations detected. Implementation plan fully aligned with Phase II constitution.

---

## Project Structure

### Documentation (this feature)

```text
specs/002-fullstack-todo-web/
├── spec.md                     # Feature specification (approved)
├── plan.md                     # This file (/sp.plan output)
├── research.md                 # Phase 0: Technical research (10 areas resolved)
├── data-model.md               # Phase 1: Entity definitions, schema, SQLModel
├── quickstart.md               # Phase 1: Development setup guide
├── contracts/                  # Phase 1: API contracts
│   ├── tasks-api.md           # RESTful tasks API specification
│   └── auth-api.md            # Better Auth integration reference
├── checklists/
│   └── requirements.md        # Quality validation checklist
└── tasks.md                   # Phase 2: /sp.tasks output (NOT created yet)
```

### Source Code (repository root)

```text
todo-fullstack/
├── console/                    # Phase I console app (preserved for reference)
│   ├── src/
│   │   ├── models.py
│   │   ├── services.py
│   │   └── cli.py
│   └── tests/
│
├── backend/                    # Phase II FastAPI backend
│   ├── src/
│   │   ├── models/            # SQLModel database models
│   │   │   ├── __init__.py
│   │   │   ├── task.py       # Task entity (see data-model.md)
│   │   │   └── user.py       # User entity (Better Auth managed)
│   │   ├── api/               # FastAPI route handlers
│   │   │   ├── __init__.py
│   │   │   ├── tasks.py      # /api/tasks endpoints
│   │   │   └── health.py     # /health endpoint
│   │   ├── auth/              # JWT validation
│   │   │   ├── __init__.py
│   │   │   └── jwt.py        # get_current_user dependency
│   │   ├── database.py        # Database connection and session management
│   │   └── init_db.py         # Schema initialization script
│   ├── tests/
│   │   ├── unit/              # Unit tests for services
│   │   ├── integration/       # API endpoint tests
│   │   └── conftest.py        # pytest fixtures
│   ├── main.py                # FastAPI app entry point
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Environment variable template
│
├── frontend/                   # Phase II Next.js frontend
│   ├── src/
│   │   ├── app/               # App Router pages
│   │   │   ├── layout.tsx    # Root layout
│   │   │   ├── page.tsx      # Landing page
│   │   │   ├── signup/
│   │   │   │   └── page.tsx  # Sign up page
│   │   │   ├── signin/
│   │   │   │   └── page.tsx  # Sign in page
│   │   │   └── tasks/
│   │   │       └── page.tsx  # Task list page (server component)
│   │   ├── components/        # React components
│   │   │   ├── TaskList.tsx  # Task list display (client component)
│   │   │   ├── TaskItem.tsx  # Individual task (client component)
│   │   │   ├── TaskForm.tsx  # Add/edit task form (client component)
│   │   │   └── Header.tsx    # Navigation header
│   │   └── lib/               # Utilities
│   │       ├── auth.ts       # Better Auth configuration
│   │       └── api.ts        # API client utilities
│   ├── tests/
│   │   └── components/        # Component tests
│   ├── public/                # Static assets
│   ├── next.config.js         # Next.js configuration
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   ├── package.json
│   └── .env.example           # Environment variable template
│
└── specs/                      # Documentation (this directory)
```

**Structure Decision**: Web application monorepo structure selected (Option 2 from template). Rationale:
- Phase I console app preserved in `/console` for reference and comparison
- Clear separation between frontend and backend for independent deployment
- Shared repository simplifies dependency management and full-stack context
- Monorepo supports future Phase III enhancements without restructuring

---

## Architectural Decisions

### 1. Authentication: Better Auth (Next.js) + JWT Validation (FastAPI)

**Decision**: Use Better Auth library in Next.js frontend for user management and JWT generation. FastAPI backend validates JWT tokens using shared secret, extracting `user_id` from token payload.

**Rationale**:
- Better Auth handles complex authentication flows (signup, signin, session management)
- JWT tokens are stateless (no database session storage needed in backend)
- Shared `BETTER_AUTH_SECRET` ensures token compatibility between frontend and backend
- Standard `Authorization: Bearer <token>` header pattern for API requests
- User ID extracted from verified JWT (`sub` claim), never from URL or request body (prevents impersonation)

**Alternatives Considered**:
- **NextAuth.js**: Similar functionality but Better Auth has superior TypeScript support and simpler JWT integration
- **Auth0/Clerk**: Third-party services add external dependencies, cost, and potential vendor lock-in
- **Custom JWT auth**: Increases security risk, development time, and maintenance burden

**Implementation Pattern**: See `research.md` section 1 for code examples.

---

### 2. Database: Neon PostgreSQL + SQLModel ORM

**Decision**: Use SQLModel ORM with async PostgreSQL driver (asyncpg) connecting to Neon serverless PostgreSQL.

**Rationale**:
- **Neon**: Serverless PostgreSQL with automatic scaling, branching, and zero-config backups
- **SQLModel**: Combines SQLAlchemy ORM (proven, mature) with Pydantic validation (type-safe)
- **Async driver**: Leverages FastAPI's async capabilities for better concurrency
- **Type safety**: SQLModel provides both runtime validation and IDE autocomplete
- **No manual migrations**: `SQLModel.metadata.create_all()` handles schema creation (sufficient for MVP)

**Alternatives Considered**:
- **SQLAlchemy alone**: More verbose, no built-in Pydantic integration, requires separate validation layer
- **Django ORM**: Not compatible with FastAPI, synchronous-only
- **Raw SQL**: Type-unsafe, manual parameterization, no ORM benefits (relationships, migrations)

**Schema**: See `data-model.md` for complete entity definitions and SQL schema.

---

### 3. Frontend: Next.js 16 App Router + Server Components

**Decision**: Use Next.js App Router with server components for data fetching, client components only for interactivity.

**Rationale**:
- **Server components**: Can securely call backend API with JWT from HTTP-only cookie (no token exposure in client)
- **Performance**: Less JavaScript shipped to client (faster page loads)
- **SEO**: Server-side rendering for better search engine indexing
- **Developer experience**: Simplified data fetching (no useEffect/loading states for initial data)
- **Client components**: Used only for forms, buttons, and interactive UI elements

**Alternatives Considered**:
- **Pages Router**: Legacy Next.js routing, less efficient data fetching, more client-side code
- **All client components**: Exposes JWT in browser JavaScript, larger bundle size, worse performance
- **Remix/SvelteKit**: Different ecosystem, steeper learning curve, less mature TypeScript support

**Pattern**: See `research.md` section 3 for implementation examples.

---

### 4. API Design: RESTful with User Context from JWT

**Decision**: RESTful API under `/api/tasks` with user_id extracted from JWT token (not in URL paths or request bodies).

**Rationale**:
- **Security**: User cannot forge or manipulate user_id (comes from cryptographically verified JWT)
- **RESTful**: Standard HTTP verbs (GET, POST, PUT, PATCH, DELETE) with proper status codes
- **Simplicity**: No `/api/users/{user_id}/tasks` nesting (user context is implicit from auth)
- **Authorization**: Every endpoint validates ownership before allowing operations
- **Error responses**: 404 for non-existent tasks (indistinguishable from unauthorized access to prevent enumeration)

**Endpoint Summary**:
- `GET /api/tasks` - List all user's tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get single task
- `PUT /api/tasks/{id}` - Update task
- `PATCH /api/tasks/{id}/toggle` - Toggle completion
- `DELETE /api/tasks/{id}` - Delete task

**Contracts**: See `contracts/tasks-api.md` for complete API specification.

---

### 5. State Management: React State + SWR (No Redux/Zustand)

**Decision**: Use React local state with SWR for data fetching and caching. No global state management library needed.

**Rationale**:
- **SWR**: Provides automatic revalidation, caching, and optimistic UI updates
- **Simplicity**: No boilerplate for simple CRUD operations
- **Built-in features**: Loading states, error handling, and revalidation out of the box
- **Server-driven state**: Task data lives on server, frontend is just a view layer
- **No over-engineering**: Redux/Zustand unnecessary for straightforward task management

**Alternatives Considered**:
- **Redux**: Overkill for simple CRUD, excessive boilerplate
- **Zustand**: Lightweight but still unnecessary for server-driven state
- **React Query**: Similar to SWR but slightly heavier (more features we don't need)

---

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER (Browser)                               │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
            Signup/Signin             View/Manage Tasks
                    │                         │
                    ↓                         ↓
┌──────────────────────────────────────────────────────────────────────┐
│                    NEXT.JS FRONTEND (localhost:3000)                  │
├──────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────┐           ┌──────────────────────────────┐  │
│  │  Better Auth       │           │  App Router Pages            │  │
│  │  (/api/auth/*)     │           │  - /signup (server)          │  │
│  │                    │           │  - /signin (server)          │  │
│  │  Endpoints:        │           │  - /tasks (server + client)  │  │
│  │  - POST /signup    │           │                              │  │
│  │  - POST /signin    │◄──────────┤  Components:                 │  │
│  │  - POST /signout   │           │  - TaskList (client)         │  │
│  │  - GET /session    │           │  - TaskForm (client)         │  │
│  │                    │           │  - TaskItem (client)         │  │
│  │  Issues JWT tokens │           │                              │  │
│  └────────────────────┘           └──────────┬───────────────────┘  │
│                                               │                      │
│  JWT stored in HTTP-only cookie               │ API calls with JWT  │
└───────────────────────────────────────────────┼──────────────────────┘
                                                │
                       Authorization: Bearer <JWT>
                                                │
                                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND (localhost:8000)                    │
├──────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │  JWT Validation Middleware (auth/jwt.py)                        │ │
│  │  - Extracts token from Authorization header                     │ │
│  │  - Validates signature using BETTER_AUTH_SECRET                 │ │
│  │  - Extracts user_id from "sub" claim                           │ │
│  └──────────────────────────┬──────────────────────────────────────┘ │
│                             │                                         │
│                             ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │  API Routes (/api/tasks/*)                                      │ │
│  │  - GET /api/tasks → list_tasks(user_id)                        │ │
│  │  - POST /api/tasks → create_task(user_id, data)                │ │
│  │  - GET /api/tasks/{id} → get_task(user_id, id)                 │ │
│  │  - PUT /api/tasks/{id} → update_task(user_id, id, data)        │ │
│  │  - PATCH /api/tasks/{id}/toggle → toggle_task(user_id, id)     │ │
│  │  - DELETE /api/tasks/{id} → delete_task(user_id, id)           │ │
│  └──────────────────────────┬──────────────────────────────────────┘ │
│                             │                                         │
│                             ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │  SQLModel ORM (models/task.py)                                  │ │
│  │  - Task entity with validation (Pydantic)                       │ │
│  │  - Automatic SQL generation                                     │ │
│  │  - Parameterized queries (SQL injection prevention)             │ │
│  └──────────────────────────┬──────────────────────────────────────┘ │
│                             │                                         │
│                             ↓                                         │
└─────────────────────────────┼─────────────────────────────────────────┘
                              │
                     asyncpg (async PostgreSQL driver)
                              │
                              ↓
┌──────────────────────────────────────────────────────────────────────┐
│                   NEON POSTGRESQL (Cloud)                             │
├──────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────┐         ┌────────────────────────────────┐  │
│  │  users             │         │  tasks                         │  │
│  │  ──────────────    │         │  ──────────────────────────    │  │
│  │  id (PK)           │◄────────┤  id (PK)                       │  │
│  │  email (UNIQUE)    │   1:N   │  user_id (FK → users.id)       │  │
│  │  password_hash     │         │  title (VARCHAR 200)           │  │
│  │  created_at        │         │  description (TEXT 5000)       │  │
│  └────────────────────┘         │  completed (BOOLEAN)           │  │
│                                 │  created_at (TIMESTAMP)        │  │
│  Indexes:                       │  updated_at (TIMESTAMP)        │  │
│  - users.email                  └────────────────────────────────┘  │
│                                                                      │
│  Indexes:                                                            │
│  - tasks.user_id (filter by owner)                                  │
│  - tasks.completed (filter by status)                               │
│                                                                      │
│  Constraint:                                                         │
│  - tasks.user_id → users.id ON DELETE CASCADE                       │
└──────────────────────────────────────────────────────────────────────┘

Legend:
→  Data flow / API call
◄─ Foreign key relationship
```

---

## Implementation Phases

### Phase 1: Monorepo Setup & Foundation

**Goal**: Establish project structure, environment configuration, and shared secrets.

**Duration**: Foundation work (no time estimates per constitution)

**Tasks**:
1. Create `/backend` directory with Python project structure
2. Create `/frontend` directory with Next.js 16 project (`npx create-next-app@latest`)
3. Install dependencies:
   - Backend: `pip install fastapi sqlmodel asyncpg python-jose[cryptography] uvicorn`
   - Frontend: `npm install better-auth next@16 react react-dom tailwindcss`
4. Create `.env.example` templates for both frontend and backend
5. Generate shared `BETTER_AUTH_SECRET` (min 32 characters): `openssl rand -base64 32`
6. Configure environment variables in `.env.local` (frontend) and `.env` (backend)
7. Add `.env*` to `.gitignore` (prevent secret leakage)
8. Verify structure matches `/sp.plan` specification

**Acceptance Criteria**:
- [ ] Both projects have valid `package.json`/`requirements.txt`
- [ ] Environment variables documented in `.env.example`
- [ ] Shared `BETTER_AUTH_SECRET` set in both environments
- [ ] Git ignores `.env` files
- [ ] `npm run dev` (frontend) and `uvicorn main:app` (backend) start without errors

**Risks**:
- **Risk**: Secret mismatch between frontend/backend → **Mitigation**: Copy-paste from single source, document clearly
- **Risk**: Wrong Next.js version installed → **Mitigation**: Explicitly specify `next@16` in package.json

---

### Phase 2: Authentication & Security Foundation

**Goal**: Implement Better Auth in Next.js and JWT validation in FastAPI.

**Tasks**:
1. Configure Better Auth in `frontend/src/lib/auth.ts`:
   - Enable JWT plugin
   - Set minimum password length (8 characters)
   - Configure email/password authentication
2. Create Better Auth API routes (`/api/auth/signup`, `/api/auth/signin`, `/api/auth/signout`)
3. Implement `get_current_user` dependency in `backend/src/auth/jwt.py`:
   - Extract token from `Authorization` header
   - Validate JWT signature using `BETTER_AUTH_SECRET`
   - Extract `user_id` from `sub` claim
   - Raise 401 on invalid/expired tokens
4. Configure CORS middleware in FastAPI (`backend/main.py`):
   - Allow origin: `http://localhost:3000`
   - Allow credentials: `true`
   - Allow all methods and headers (development only)
5. Create test user via signup page
6. Verify JWT token in browser cookies (DevTools → Application → Cookies)

**Acceptance Criteria**:
- [ ] User can sign up with email/password (min 8 chars)
- [ ] User can sign in with valid credentials
- [ ] Invalid credentials return "Invalid email or password" error
- [ ] JWT token stored in HTTP-only cookie
- [ ] FastAPI health endpoint (`/health`) returns 200
- [ ] FastAPI protected endpoint returns 401 without valid token
- [ ] FastAPI protected endpoint returns 200 with valid token and extracts correct `user_id`

**Risks**:
- **Risk**: CORS errors in browser → **Mitigation**: Test with `curl` first, verify CORS config matches frontend URL
- **Risk**: Token validation fails → **Mitigation**: Log JWT payload in backend, verify `BETTER_AUTH_SECRET` matches

---

### Phase 3: Database Schema & Models

**Goal**: Create PostgreSQL database schema and SQLModel entities.

**Tasks**:
1. Set up Neon PostgreSQL account and create project: `todo-fullstack-dev`
2. Copy connection string and update `backend/.env`:
   - Convert `postgresql://` → `postgresql+asyncpg://`
   - Add `?sslmode=require` if missing
3. Create `backend/src/database.py`:
   - Async engine creation
   - Session dependency for FastAPI
   - `init_db()` function for schema creation
4. Create `backend/src/models/task.py`:
   - SQLModel `Task` class (see `data-model.md` lines 145-166)
   - Fields: id, user_id, title, description, completed, created_at, updated_at
   - Validation: title (1-200 chars), description (0-5000 chars)
5. Create `backend/src/init_db.py` script:
   - Runs `SQLModel.metadata.create_all()`
   - Creates `users` and `tasks` tables
   - Creates indexes on `user_id`, `completed`, `email`
6. Run database initialization: `python -m src.init_db`
7. Verify schema in Neon dashboard SQL Editor

**Acceptance Criteria**:
- [ ] Neon database accessible via connection string
- [ ] `users` table exists with correct schema
- [ ] `tasks` table exists with correct schema
- [ ] Foreign key constraint: `tasks.user_id → users.id ON DELETE CASCADE`
- [ ] Indexes created on `tasks.user_id`, `tasks.completed`, `users.email`
- [ ] SQLModel `Task` class validates field lengths correctly
- [ ] Database connection succeeds from FastAPI

**Risks**:
- **Risk**: Connection string format wrong → **Mitigation**: Test with `psql` command first
- **Risk**: Better Auth creates incompatible user schema → **Mitigation**: Review Better Auth docs, may need manual user table creation

**Reference**: See `data-model.md` for complete schema and validation rules.

---

### Phase 4: Backend API Implementation

**Goal**: Implement all 6 task management endpoints with ownership validation.

**Tasks**:
1. Create `backend/src/api/tasks.py` with route handlers:
   - `GET /api/tasks` → `list_tasks(user_id)`
   - `POST /api/tasks` → `create_task(user_id, request)`
   - `GET /api/tasks/{task_id}` → `get_task(user_id, task_id)`
   - `PUT /api/tasks/{task_id}` → `update_task(user_id, task_id, request)`
   - `PATCH /api/tasks/{task_id}/toggle` → `toggle_completion(user_id, task_id)`
   - `DELETE /api/tasks/{task_id}` → `delete_task(user_id, task_id)`
2. All endpoints must:
   - Use `Depends(get_current_user)` to extract `user_id` from JWT
   - Filter queries by `user_id` (prevent cross-user access)
   - Return 404 if task not found OR belongs to different user (indistinguishable)
   - Validate request bodies using Pydantic models (TaskCreateRequest, TaskUpdateRequest)
   - Return TaskResponse Pydantic model (automatic JSON serialization)
3. Create Pydantic request/response models (see `data-model.md` lines 172-208)
4. Register routes in `backend/main.py`
5. Test all endpoints using FastAPI Swagger UI (`/docs`)

**Acceptance Criteria**:
- [ ] `GET /api/tasks` returns only authenticated user's tasks
- [ ] `POST /api/tasks` creates task with correct `user_id`
- [ ] `PUT /api/tasks/{id}` updates task only if owned by user (403 otherwise)
- [ ] `PATCH /api/tasks/{id}/toggle` toggles completion status
- [ ] `DELETE /api/tasks/{id}` removes task only if owned by user
- [ ] Validation errors return 400 with clear messages
- [ ] Missing/invalid JWT returns 401
- [ ] Cross-user access attempts return 404 (not 403)
- [ ] All endpoints accessible via Swagger UI at `/docs`

**Risks**:
- **Risk**: SQL injection vulnerability → **Mitigation**: SQLModel uses parameterized queries (verify no raw SQL)
- **Risk**: User can access other users' tasks → **Mitigation**: Multi-user integration test required

**Reference**: See `contracts/tasks-api.md` for complete endpoint specifications.

---

### Phase 5: Frontend Task UI & Integration

**Goal**: Build Next.js task management UI with full backend integration.

**Tasks**:
1. Create protected route middleware (`frontend/src/middleware.ts`):
   - Check for `auth-token` cookie
   - Redirect to `/signin` if missing
   - Verify token expiration (handle expired tokens per FR-036)
2. Create signup page (`frontend/src/app/signup/page.tsx`):
   - Email + password form (client component)
   - Validation: email format, password min 8 chars
   - Call `/api/auth/signup`
   - Redirect to `/tasks` on success
3. Create signin page (`frontend/src/app/signin/page.tsx`):
   - Email + password form
   - Call `/api/auth/signin`
   - Display "Invalid email or password" on failure
   - Redirect to `/tasks` on success
4. Create tasks page (`frontend/src/app/tasks/page.tsx`):
   - Server component: fetches tasks from `GET /api/tasks` with JWT
   - Passes tasks to client component
   - Handles empty state ("No tasks yet. Add your first task to get started!")
5. Create TaskList component (`frontend/src/components/TaskList.tsx`):
   - Client component (interactive UI)
   - Displays tasks with title, status, truncated description (100 chars)
   - Toggle completion via `PATCH /api/tasks/{id}/toggle`
   - Delete task via `DELETE /api/tasks/{id}`
   - Edit task inline or via modal
6. Create TaskForm component (`frontend/src/components/TaskForm.tsx`):
   - Client component
   - Input: title (required, max 200 chars), description (optional, max 5000 chars)
   - Validation with error messages
   - Call `POST /api/tasks` on submit
   - Clear form on success
7. Implement token expiration handling (FR-036):
   - Preserve unsaved work in session storage
   - Redirect to signin with message on 401
   - Restore unsaved work after re-authentication
8. Style with Tailwind CSS (responsive design)

**Acceptance Criteria**:
- [ ] Unauthenticated users redirected to `/signin`
- [ ] User can sign up and automatically sign in
- [ ] User can sign in with existing account
- [ ] Tasks page displays user's tasks (newest first)
- [ ] Empty state shown when no tasks exist
- [ ] User can create task with title only
- [ ] User can create task with title + description
- [ ] Description truncated at 100 chars with ellipsis in list view
- [ ] User can toggle task completion (visual feedback)
- [ ] User can delete task (with confirmation)
- [ ] User can update task title/description
- [ ] Validation errors displayed for empty title, excess length
- [ ] UI responsive on mobile (375px) and desktop (1920px)
- [ ] Token expiration redirects to signin with preserved work

**Risks**:
- **Risk**: Token exposed in client JavaScript → **Mitigation**: Use server components for data fetching, cookie-based auth
- **Risk**: XSS vulnerability in task content → **Mitigation**: React auto-escapes output, verify no `dangerouslySetInnerHTML`

**Reference**: See `contracts/tasks-api.md` for API integration patterns.

---

### Phase 6: Polish & User Experience

**Goal**: Enhance UX with loading states, optimistic updates, and error handling.

**Tasks**:
1. Add loading states:
   - Skeleton loaders for task list
   - Button spinners during API calls
   - Disable form inputs during submission
2. Implement optimistic UI updates:
   - Task appears immediately in list before server confirmation
   - Rollback on error
3. Error handling:
   - Display user-friendly error messages (no stack traces)
   - Toast notifications for success/error
   - Retry mechanism for failed requests
4. Accessibility:
   - Keyboard navigation (Tab, Enter, Escape)
   - ARIA labels for screen readers
   - Focus management (e.g., focus input after modal open)
5. Performance optimization:
   - SWR caching for task list
   - Debounce search/filter inputs (if added)
   - Lazy load large task lists (if >100 tasks)

**Acceptance Criteria**:
- [ ] Loading spinners shown during API calls
- [ ] Optimistic updates work for toggle, delete, create
- [ ] Errors display friendly messages (not JSON blobs)
- [ ] Success toast shown after create/update/delete
- [ ] Keyboard shortcuts work (Enter to submit, Escape to close modal)
- [ ] Screen reader announces task status changes
- [ ] Task list loads in <2 seconds for 100 tasks

**Risks**:
- **Risk**: Optimistic updates cause state desync → **Mitigation**: Use SWR's mutate API with rollback
- **Risk**: Accessibility issues → **Mitigation**: Test with screen reader, keyboard-only navigation

---

### Phase 7: Testing & Validation

**Goal**: Comprehensive testing across unit, integration, and E2E layers.

**Tasks**:
1. **Backend Unit Tests** (`backend/tests/unit/`):
   - Task model validation (field lengths, required fields)
   - JWT validation logic (expired token, invalid signature)
   - Database query functions
2. **Backend Integration Tests** (`backend/tests/integration/`):
   - All API endpoints with real database (test database)
   - Multi-user isolation (User A cannot access User B's tasks)
   - Error cases (404, 401, 400, 500)
   - Concurrent requests (50 users creating tasks simultaneously)
3. **Frontend Component Tests** (`frontend/tests/components/`):
   - TaskList renders tasks correctly
   - TaskForm validation works
   - Button click handlers fire
4. **E2E Tests** (Playwright or Cypress):
   - Full user journey: signup → create task → toggle → delete → signout
   - Multi-user isolation (two browser contexts)
   - Token expiration handling
5. **Security Testing**:
   - SQL injection attempts (should fail)
   - XSS attempts (should be escaped)
   - CSRF protection (SameSite cookies)
   - Cross-user access attempts (should return 404)
6. **Performance Testing**:
   - Load test: 50 concurrent users
   - Task list with 1000 tasks (should load in <2 seconds)
7. Run full test suite: `pytest backend/tests/ && npm test`

**Acceptance Criteria**:
- [ ] All backend unit tests pass (>90% coverage)
- [ ] All backend integration tests pass
- [ ] All frontend component tests pass
- [ ] E2E tests pass for happy path and error cases
- [ ] Multi-user isolation verified (no data leakage)
- [ ] Security tests pass (no SQL injection, XSS, CSRF)
- [ ] Performance tests meet SLA (<2s task list, 50 concurrent users)

**Risks**:
- **Risk**: Test database pollution → **Mitigation**: Use pytest fixtures to reset DB between tests
- **Risk**: Flaky E2E tests → **Mitigation**: Add explicit waits, retry logic

---

### Phase 8: Final Deliverables & Documentation

**Goal**: Prepare production-ready deployment and comprehensive documentation.

**Tasks**:
1. **Production Environment Configuration**:
   - Update CORS origins to production domain
   - Set `secure: true` for cookies (HTTPS only)
   - Disable SQL query logging
   - Set production `DATABASE_URL` (Neon production branch)
2. **Deployment Preparation**:
   - Frontend: Vercel/Netlify configuration
   - Backend: Dockerfile for FastAPI + deployment config (Render/Railway)
   - Environment variable setup in hosting platforms
3. **Documentation**:
   - Update `quickstart.md` with production deployment steps
   - Create `DEPLOYMENT.md` with hosting instructions
   - Document environment variables in `README.md`
4. **Final Testing**:
   - Smoke test on production environment
   - Verify HTTPS certificate
   - Test from multiple devices (mobile, desktop, different browsers)
5. **Code Quality**:
   - Run linters (ESLint, Black)
   - Fix type errors (TypeScript strict mode, mypy)
   - Remove console.logs and debug statements
6. **Create ADR** (if architecturally significant decisions were made):
   - Run `/sp.adr <decision-title>` for JWT auth approach
   - Document alternatives considered and rationale

**Acceptance Criteria**:
- [ ] Production environment deployed and accessible
- [ ] HTTPS enabled (SSL certificate valid)
- [ ] All environment variables configured in production
- [ ] Deployment documentation complete
- [ ] Code passes linters and type checkers
- [ ] Smoke tests pass on production
- [ ] ADR created for major architectural decisions (if applicable)

**Risks**:
- **Risk**: Environment variable mismatch in production → **Mitigation**: Checklist of required vars, validate on startup
- **Risk**: CORS fails in production → **Mitigation**: Test with actual production URL before launch

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation Strategy | Owner |
|------|-------------|--------|---------------------|-------|
| **JWT secret mismatch** | Medium | High | Use single source of truth (`.env.example`), copy-paste, document clearly, validate on startup | Backend Dev |
| **User data leakage** | Low | Critical | Multi-user integration tests, code review of all queries, verify `user_id` filtering | Backend Dev + QA |
| **Database connection pool exhaustion** | Low | High | Use async sessions, proper cleanup (`async with`), load testing with 50+ users | Backend Dev |
| **CORS configuration errors** | Medium | Medium | Test from actual Next.js dev server, document origins, validate CORS headers | Backend Dev |
| **Token expiration during active session** | Medium | Medium | Implement session storage for unsaved work (FR-036), test with short token expiry (5 min) | Frontend Dev |
| **Better Auth incompatibility with FastAPI** | Low | High | Prototype JWT validation early (Phase 2), verify token payload structure | Backend Dev |
| **SQL injection vulnerability** | Low | Critical | Use SQLModel ORM exclusively, no raw SQL, security testing | Backend Dev + Security |
| **XSS attack via task content** | Low | High | Verify React auto-escaping, no `dangerouslySetInnerHTML`, security testing | Frontend Dev + Security |
| **Performance degradation with large task lists** | Medium | Medium | Index on `user_id`, test with 1000 tasks, pagination if needed (Phase III) | Backend Dev |
| **Neon database downtime** | Low | Medium | Monitor Neon status, have backup connection string, plan migration strategy | DevOps |

---

## Dependencies & Execution Order

### Critical Path

```
Phase 1 (Monorepo Setup)
    ↓
Phase 2 (Authentication) ← Must complete before Phase 4
    ↓
Phase 3 (Database Schema) ← Must complete before Phase 4
    ↓
Phase 4 (Backend API) ← Must complete before Phase 5
    ↓
Phase 5 (Frontend UI) ← Depends on Phase 4
    ↓
Phase 6 (UX Polish) ← Can start after Phase 5 MVP
    ↓
Phase 7 (Testing) ← Can run in parallel with Phase 6
    ↓
Phase 8 (Deployment) ← Requires all previous phases complete
```

### Parallelizable Work

- **Phase 3 and Phase 2** can partially overlap (database schema design while implementing auth)
- **Phase 6 and Phase 7** can run concurrently (polish frontend while writing tests)
- **Documentation** (Phase 8) can be written incrementally during implementation

### External Dependencies

- **Neon PostgreSQL**: Account creation and database provisioning (Phase 3)
- **Better Auth**: Library installation and configuration (Phase 2)
- **Hosting platforms**: Vercel/Render account setup (Phase 8)

---

## Success Gate

Implementation plan is ready when ALL of the following conditions are met:

- ✅ **Constitution Check**: All 7 principles validated (see Constitution Check section above)
- ✅ **Research Complete**: All 10 technical unknowns resolved (see `research.md`)
- ✅ **Data Model Finalized**: Entity definitions, schema, and SQLModel classes documented (see `data-model.md`)
- ✅ **API Contracts Defined**: All 6 task endpoints specified with request/response formats (see `contracts/tasks-api.md`)
- ✅ **Quickstart Guide Available**: Development environment setup documented (see `quickstart.md`)
- ✅ **Project Structure Confirmed**: Monorepo layout matches specification (see Project Structure section)
- ✅ **Phases Defined**: All 8 implementation phases with clear acceptance criteria (see Implementation Phases)
- ✅ **Risks Identified**: Top 10 risks with mitigation strategies (see Risk Assessment)

**Current Status**: ✅ **ALL GATES PASSED** - Ready to proceed to `/sp.tasks` for task breakdown.

---

## Next Steps

1. **User Review**: Review this implementation plan for completeness and accuracy
2. **Generate Tasks**: Run `/sp.tasks` to create actionable, dependency-ordered tasks from this plan
3. **ADR Creation** (optional): If user identifies architecturally significant decisions, run `/sp.adr <decision-title>` to document
4. **Begin Implementation**: Start with Phase 1 (Monorepo Setup & Foundation)

---

## Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-01-02 | 1.0.0 | Initial implementation plan created via `/sp.plan` command | Claude Sonnet 4.5 |
