# Technical Research: Multi-User Full-Stack Todo Web Application

**Feature**: 002-fullstack-todo-web
**Date**: 2026-01-02
**Purpose**: Resolve all technical unknowns and establish architectural foundation for Phase II implementation

## Research Areas

### 1. Better Auth + FastAPI Integration

**Decision**: Use Better Auth (Next.js) for user management with JWT plugin; FastAPI validates JWT using PyJWT library with shared secret

**Rationale**:
- Better Auth handles user registration, authentication, and JWT generation
- FastAPI remains stateless (no session management)
- Shared `BETTER_AUTH_SECRET` ensures token compatibility
- Standard `Authorization: Bearer <token>` header pattern
- User ID extracted from verified JWT payload, not from URL or request body

**Alternatives Considered**:
- NextAuth.js: Similar but Better Auth has better TypeScript support and simpler JWT integration
- Auth0/Clerk: Third-party services add external dependencies and cost
- Custom auth: Increases security risk and development time

**Implementation Pattern**:
```python
# FastAPI dependency for JWT verification
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, Header

async def get_current_user(authorization: str = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
```

---

### 2. Neon PostgreSQL Connection Best Practices

**Decision**: Use SQLModel with async PostgreSQL driver (asyncpg) for Neon serverless PostgreSQL

**Rationale**:
- Neon provides serverless PostgreSQL with automatic scaling
- SQLModel combines SQLAlchemy ORM with Pydantic validation
- Async driver leverages FastAPI's async capabilities
- Connection pooling handled automatically
- No manual schema migrations needed (SQLModel.metadata.create_all())

**Alternatives Considered**:
- SQLAlchemy alone: More verbose, no built-in Pydantic integration
- Django ORM: Not compatible with FastAPI
- Raw SQL: Type-unsafe, manual parameterization, no ORM benefits

**Implementation Pattern**:
```python
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL")  # postgresql+asyncpg://...

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session
```

---

### 3. Next.js 16 App Router + Server Components

**Decision**: Use App Router with server components for data fetching, client components only for interactivity

**Rationale**:
- Server components can securely call backend API with JWT (no client exposure)
- Better performance (less JavaScript shipped to client)
- SEO-friendly server-side rendering
- Client components used only for forms, buttons, interactive UI

**Alternatives Considered**:
- Pages Router: Legacy, less efficient data fetching
- All client components: Exposes JWT in browser, larger bundle size
- Remix/SvelteKit: Different ecosystem, steeper learning curve

**Implementation Pattern**:
```typescript
// app/tasks/page.tsx (Server Component)
import { cookies } from 'next/headers';

export default async function TasksPage() {
  const token = cookies().get('auth-token')?.value;

  const response = await fetch('http://localhost:8000/api/tasks', {
    headers: { 'Authorization': `Bearer ${token}` }
  });

  const tasks = await response.json();
  return <TaskList tasks={tasks} />; // Pass to Client Component
}

// components/TaskList.tsx ('use client' for interactivity)
'use client';
export function TaskList({ tasks }) {
  // Interactive UI: delete, toggle, edit
}
```

---

### 4. Monorepo Structure & Development Workflow

**Decision**: Single monorepo with `/console`, `/frontend`, `/backend` directories; separate dev servers running concurrently

**Rationale**:
- Single repository simplifies dependency management
- Frontend and backend share type definitions (via shared package if needed)
- Phase I code preserved in `/console` for reference
- Claude Code maintains full context across layers

**Alternatives Considered**:
- Separate repos: Complicates versioning and deployment
- Polyrepo with Git submodules: Added complexity, poor DX
- Lerna/Nx monorepo tools: Overkill for two-service project

**Development Workflow**:
1. Terminal 1: `cd frontend && npm run dev` (Next.js on port 3000)
2. Terminal 2: `cd backend && uvicorn main:app --reload` (FastAPI on port 8000)
3. Frontend proxies `/api/*` requests to backend via `next.config.js` rewrites

---

### 5. CORS Configuration

**Decision**: Configure FastAPI CORS middleware to allow requests from Next.js dev server (localhost:3000) and production domain

**Rationale**:
- Development: Next.js (localhost:3000) calls FastAPI (localhost:8000)
- Production: Same origin or explicit CORS policy
- Preflight requests handled automatically by FastAPI middleware

**Implementation Pattern**:
```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 6. Environment Variable Management

**Decision**: Use `.env` files for both frontend and backend with `.env.example` templates committed to repo

**Rationale**:
- Secrets never committed (`.env` in `.gitignore`)
- `.env.example` documents required variables
- Same `BETTER_AUTH_SECRET` used in both frontend and backend
- Neon DATABASE_URL stored securely

**Required Variables**:

**Frontend `.env.local`**:
```bash
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend `.env`**:
```bash
BETTER_AUTH_SECRET=your-secret-key-min-32-chars  # MUST match frontend
DATABASE_URL=postgresql+asyncpg://user:pass@neon-host/dbname
CORS_ORIGINS=http://localhost:3000
```

---

### 7. Task Data Model Design

**Decision**: SQLModel `Task` model with user_id foreign key, created_at/updated_at timestamps, proper indexes

**Rationale**:
- Foreign key ensures referential integrity (CASCADE DELETE)
- Indexes on user_id and completed for query performance
- SQLModel provides both ORM and Pydantic validation
- Timestamps track task lifecycle

**Schema**:
```python
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200, min_length=1)
    description: str | None = Field(default=None, max_length=5000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

### 8. API Error Handling Pattern

**Decision**: FastAPI exception handlers with consistent error response format

**Rationale**:
- Standardized error responses across all endpoints
- HTTP status codes follow REST conventions
- User-friendly messages (no stack traces)
- Validation errors return field-specific details

**Implementation Pattern**:
```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

# Usage in endpoints:
if not task:
    raise HTTPException(status_code=404, detail="Task not found")
if task.user_id != current_user_id:
    raise HTTPException(status_code=403, detail="Not authorized to access this task")
```

---

### 9. Frontend State Management

**Decision**: React state with SWR for data fetching and caching (no Redux/Zustand needed)

**Rationale**:
- SWR provides automatic revalidation and caching
- Optimistic UI updates for better UX
- Built-in error handling and loading states
- No additional global state needed for simple CRUD

**Alternatives Considered**:
- Redux: Overkill for simple task management
- Zustand: Unnecessary for server-driven state
- React Query: Similar to SWR, slightly heavier

---

### 10. Password Security

**Decision**: Better Auth handles password hashing with bcrypt (12 rounds)

**Rationale**:
- Better Auth uses industry-standard bcrypt by default
- No manual password handling in application code
- Passwords never stored in plain text
- 8-character minimum enforced client-side and server-side

---

## Technology Stack Summary

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend** | Next.js | 16+ | React framework with App Router |
| **Frontend** | TypeScript | 5.x | Type-safe JavaScript |
| **Frontend** | Tailwind CSS | 3.x | Utility-first CSS |
| **Frontend** | Better Auth | Latest | User authentication + JWT |
| **Backend** | FastAPI | 0.115+ | High-performance async API |
| **Backend** | SQLModel | 0.0.22+ | ORM with Pydantic validation |
| **Backend** | Python | 3.13+ | Backend language |
| **Backend** | PyJWT | 2.x | JWT token verification |
| **Backend** | asyncpg | 0.30+ | Async PostgreSQL driver |
| **Database** | Neon PostgreSQL | Latest | Serverless PostgreSQL |

---

## Risk Mitigation

| Risk | Mitigation Strategy | Verification |
|------|-------------------|--------------|
| JWT secret mismatch between frontend/backend | Use same `.env` variable name, document clearly | Test full auth flow end-to-end |
| User data leakage | Enforce user_id filtering in all queries | Multi-user integration tests |
| Database connection pool exhaustion | Use async sessions with proper cleanup | Load testing with 50+ concurrent users |
| CORS configuration errors | Test from actual Next.js dev server | Manual browser testing with network tab |
| Token expiration during active session | Implement session storage for unsaved work | Test with short token expiry (5 min) |

---

## Development Environment Setup

### Prerequisites
- Node.js 20+ (for Next.js)
- Python 3.13+ (for FastAPI)
- PostgreSQL client (for database access)
- Neon account (for cloud PostgreSQL)

### Local Development Steps
1. Clone repository
2. Copy `.env.example` to `.env.local` (frontend) and `.env` (backend)
3. Set `BETTER_AUTH_SECRET` to same value in both
4. Create Neon database and set `DATABASE_URL`
5. Install dependencies: `npm install` (frontend), `pip install -r requirements.txt` (backend)
6. Run dev servers concurrently

---

## Unresolved Items

None - All technical unknowns from specification have been researched and resolved.

---

## Next Steps

1. Create `data-model.md` with complete entity definitions
2. Generate API contracts in `/contracts/`
3. Write `quickstart.md` for development setup
4. Begin implementation with Phase 1 (Monorepo Setup)
