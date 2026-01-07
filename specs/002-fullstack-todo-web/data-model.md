# Data Model: Multi-User Full-Stack Todo Web Application

**Feature**: 002-fullstack-todo-web
**Date**: 2026-01-02
**Purpose**: Define database schema, entities, relationships, and validation rules

## Entity Relationship Diagram

```
┌─────────────────────────┐
│ users (Better Auth)     │
│─────────────────────────│
│ id: TEXT (PK)           │
│ email: TEXT (UNIQUE)    │
│ password_hash: TEXT     │
│ created_at: TIMESTAMP   │
└───────────┬─────────────┘
            │
            │ 1:N
            ↓
┌───────────────────────────┐
│ tasks                     │
│───────────────────────────│
│ id: SERIAL (PK)           │
│ user_id: TEXT (FK)        │<── Foreign Key: users.id ON DELETE CASCADE
│ title: VARCHAR(200)       │
│ description: TEXT         │
│ completed: BOOLEAN        │
│ created_at: TIMESTAMP     │
│ updated_at: TIMESTAMP     │
└───────────────────────────┘

Indexes:
- tasks.user_id (for user-specific queries)
- tasks.completed (for status filtering)
- users.email (for login lookups)
```

---

## Entity Definitions

### 1. User (Managed by Better Auth)

**Purpose**: Represents an authenticated user account

**Attributes**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | TEXT | PRIMARY KEY | Unique user identifier (UUID from Better Auth) |
| `email` | TEXT | UNIQUE, NOT NULL | User's email address (login credential) |
| `password_hash` | TEXT | NOT NULL | Bcrypt-hashed password (min 8 chars before hashing) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |

**Validation Rules**:
- Email must be valid email format (validated by Better Auth)
- Password minimum 8 characters (enforced before hashing)
- Email uniqueness enforced at database level

**Relationships**:
- One user can have many tasks (1:N)

**Notes**:
- Managed entirely by Better Auth library
- No direct modification from application code
- User deletion cascades to tasks (removes orphaned data)

---

### 2. Task

**Purpose**: Represents a single todo item belonging to a user

**Attributes**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Auto-incrementing unique task identifier |
| `user_id` | TEXT | FOREIGN KEY (users.id), NOT NULL, INDEX | Owner of this task |
| `title` | VARCHAR(200) | NOT NULL, MIN 1, MAX 200 | Task title (required) |
| `description` | TEXT | NULL, MAX 5000 | Optional task description |
| `completed` | BOOLEAN | NOT NULL, DEFAULT FALSE, INDEX | Completion status |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Task creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last modification timestamp |

**Validation Rules**:
- **Title**: 1-200 characters, non-empty, non-whitespace only
- **Description**: 0-5000 characters, nullable
- **User ID**: Must reference existing user (foreign key constraint)
- **Completed**: Boolean only (true/false)

**Relationships**:
- Each task belongs to exactly one user (N:1)
- Foreign key constraint: `user_id` → `users.id` ON DELETE CASCADE

**Indexes**:
- Primary key on `id` (automatic)
- Index on `user_id` (optimize user-specific queries: `WHERE user_id = ?`)
- Index on `completed` (optimize status filtering)

**Business Rules**:
- Task can only be accessed by owner (user_id must match authenticated user)
- Task can be deleted regardless of completion status
- Completed tasks can be unmarked (toggle between pending/completed)
- Updated_at timestamp refreshes on any field modification

---

## Database Schema (SQL)

```sql
-- users table (managed by Better Auth)
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL CHECK (length(trim(title)) > 0),
    description TEXT CHECK (length(description) <= 5000),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_users_email ON users(email);
```

---

## SQLModel Definitions (Python)

```python
from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """Task entity with user ownership and validation."""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True, nullable=False)
    title: str = Field(min_length=1, max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=5000)
    completed: bool = Field(default=False, index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user-uuid-123",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False
            }
        }
```

---

## Pydantic Request/Response Models

### Task Creation Request
```python
from pydantic import BaseModel, Field

class TaskCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200, description="Task title")
    description: str | None = Field(default=None, max_length=5000, description="Optional description")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Call dentist",
                "description": "Schedule annual checkup"
            }
        }
```

### Task Update Request
```python
class TaskUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
```

### Task Response
```python
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows creation from ORM models
```

---

## State Transitions

### Task Lifecycle

```
[CREATE] → PENDING (default)
             │
             ↓
    ┌────────┴────────┐
    ↓                 ↓
PENDING ←──────→ COMPLETED
    │                 │
    ↓                 ↓
[UPDATE/DELETE]  [UPDATE/DELETE]
```

**Valid Transitions**:
1. **Create** → Pending (automatic, default completed=false)
2. **Pending** → Completed (user marks complete)
3. **Completed** → Pending (user unmarks / toggles back)
4. **Any State** → Deleted (user deletes task)
5. **Any State** → Updated (user modifies title/description)

**No Invalid States**: System enforces boolean completed field (no "archived", "in-progress", etc.)

---

## Data Access Patterns

### Common Queries

1. **Get all tasks for user**:
```sql
SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC;
```

2. **Get single task (with ownership check)**:
```sql
SELECT * FROM tasks WHERE id = ? AND user_id = ?;
```

3. **Create task**:
```sql
INSERT INTO tasks (user_id, title, description, completed, created_at, updated_at)
VALUES (?, ?, ?, false, NOW(), NOW()) RETURNING *;
```

4. **Update task**:
```sql
UPDATE tasks SET title = ?, description = ?, updated_at = NOW()
WHERE id = ? AND user_id = ? RETURNING *;
```

5. **Toggle completion**:
```sql
UPDATE tasks SET completed = NOT completed, updated_at = NOW()
WHERE id = ? AND user_id = ? RETURNING *;
```

6. **Delete task**:
```sql
DELETE FROM tasks WHERE id = ? AND user_id = ?;
```

**Performance Considerations**:
- All queries filtered by `user_id` (uses index)
- Order by `created_at DESC` for newest-first display
- `RETURNING *` clause avoids extra SELECT query after mutations

---

## Security Considerations

1. **User Isolation**:
   - All queries include `AND user_id = ?` clause
   - Foreign key CASCADE DELETE prevents orphaned tasks
   - No cross-user data leakage possible

2. **SQL Injection Prevention**:
   - SQLModel uses parameterized queries (automatic)
   - No string concatenation for SQL
   - All user input sanitized through Pydantic validation

3. **Data Integrity**:
   - Foreign key constraints enforce referential integrity
   - CHECK constraints prevent invalid lengths
   - NOT NULL constraints prevent missing required fields

---

## Migration Strategy

**Initial Schema Creation**:
```python
from sqlmodel import SQLModel, create_engine

async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

**Future Migrations**:
- Use Alembic for schema changes (not needed for MVP)
- Example: Adding new fields, indexes, or constraints

---

## Testing Data

### Sample Users
```python
user_alice = {
    "id": "alice-uuid-123",
    "email": "alice@example.com",
    "password_hash": "$2b$12$..." # bcrypt hash
}

user_bob = {
    "id": "bob-uuid-456",
    "email": "bob@example.com",
    "password_hash": "$2b$12$..."
}
```

### Sample Tasks
```python
alice_tasks = [
    {"user_id": "alice-uuid-123", "title": "Buy groceries", "description": "Milk, eggs", "completed": False},
    {"user_id": "alice-uuid-123", "title": "Call dentist", "description": None, "completed": True}
]

bob_tasks = [
    {"user_id": "bob-uuid-456", "title": "Write report", "description": "Q4 summary", "completed": False}
]
```

**Isolation Test**: Alice cannot access/modify Bob's tasks (403 Forbidden)

---

## Summary

- **2 entities**: User (Better Auth), Task (application)
- **1 relationship**: User → Tasks (1:N with CASCADE DELETE)
- **7 fields per task**: id, user_id, title, description, completed, created_at, updated_at
- **3 indexes**: tasks.user_id, tasks.completed, users.email
- **Type-safe**: SQLModel for ORM, Pydantic for API validation
- **Secure**: Foreign keys, user isolation, parameterized queries
