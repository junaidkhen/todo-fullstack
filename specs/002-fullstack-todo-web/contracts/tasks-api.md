# API Contract: Tasks API

**Feature**: 002-fullstack-todo-web
**Date**: 2026-01-02
**Purpose**: RESTful API specification for task management operations

## Base URL

```
Development: http://localhost:8000
Production: https://api.yourdomain.com
```

## Authentication

All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

**Token Source**: Issued by Better Auth (Next.js frontend)
**Validation**: FastAPI backend validates using shared `BETTER_AUTH_SECRET`
**User Context**: `user_id` extracted from JWT payload (`sub` claim), never from request body or URL

## Common Response Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PUT, PATCH operations |
| 201 | Created | Successful POST operations |
| 204 | No Content | Successful DELETE operations |
| 400 | Bad Request | Invalid input data (validation errors) |
| 401 | Unauthorized | Missing/invalid JWT token |
| 403 | Forbidden | Valid token but user doesn't own the resource |
| 404 | Not Found | Resource doesn't exist or user doesn't have access |
| 500 | Internal Server Error | Server-side errors |

## Error Response Format

All error responses follow this structure:

```json
{
  "error": "Human-readable error message"
}
```

**Examples**:
```json
{"error": "Missing or invalid token"}
{"error": "Task not found"}
{"error": "Not authorized to access this task"}
{"error": "Title cannot be empty"}
{"error": "Title cannot exceed 200 characters"}
```

---

## Endpoints

### 1. List All Tasks for Current User

**Endpoint**: `GET /api/tasks`

**Description**: Retrieves all tasks belonging to the authenticated user, ordered by creation date (newest first).

**Authentication**: Required (JWT)

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Request Body**: None

**Success Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-01-02T10:30:00Z",
    "updated_at": "2026-01-02T10:30:00Z"
  },
  {
    "id": 2,
    "title": "Call dentist",
    "description": null,
    "completed": true,
    "created_at": "2026-01-01T15:20:00Z",
    "updated_at": "2026-01-02T09:15:00Z"
  }
]
```

**Empty List Response** (200 OK):
```json
[]
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT token
- `500 Internal Server Error`: Database connection failure

**Notes**:
- Tasks are automatically filtered by `user_id` extracted from JWT (no cross-user data leakage)
- No pagination required for MVP (optimize for up to 1000 tasks per user)
- Returns empty array if user has no tasks

---

### 2. Get Single Task

**Endpoint**: `GET /api/tasks/{task_id}`

**Description**: Retrieves a specific task by ID. Only returns task if it belongs to the authenticated user.

**Authentication**: Required (JWT)

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `task_id` | integer | Unique task identifier |

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-02T10:30:00Z",
  "updated_at": "2026-01-02T10:30:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT token
- `404 Not Found`: Task doesn't exist OR task belongs to different user (indistinguishable for security)

**Security Note**: System returns 404 (not 403) when task belongs to another user to prevent task ID enumeration attacks.

---

### 3. Create New Task

**Endpoint**: `POST /api/tasks`

**Description**: Creates a new task for the authenticated user. Task is automatically associated with the user from JWT token.

**Authentication**: Required (JWT)

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Request Schema**:
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `title` | string | Yes | 1-200 chars, non-whitespace | Task title |
| `description` | string | No | 0-5000 chars | Task description (nullable) |

**Success Response** (201 Created):
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-02T10:30:00Z",
  "updated_at": "2026-01-02T10:30:00Z"
}
```

**Validation Error Response** (400 Bad Request):
```json
{"error": "Title cannot be empty"}
{"error": "Title cannot exceed 200 characters"}
{"error": "Description cannot exceed 5000 characters"}
```

**Error Responses**:
- `400 Bad Request`: Validation errors (see examples above)
- `401 Unauthorized`: Missing or invalid JWT token
- `500 Internal Server Error`: Database write failure

**Notes**:
- `user_id` is automatically extracted from JWT token (not in request body)
- `completed` defaults to `false` (cannot be set during creation)
- `created_at` and `updated_at` are auto-generated server-side
- `description` is optional (defaults to `null` if omitted)

---

### 4. Update Task (Full Update)

**Endpoint**: `PUT /api/tasks/{task_id}`

**Description**: Updates an existing task's title and/or description. Only succeeds if task belongs to authenticated user.

**Authentication**: Required (JWT)

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `task_id` | integer | Unique task identifier |

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Team Meeting at 3pm",
  "description": "Prepare presentation slides"
}
```

**Request Schema**:
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `title` | string | No | 1-200 chars, non-whitespace | Updated task title |
| `description` | string | No | 0-5000 chars | Updated description (nullable) |

**Success Response** (200 OK):
```json
{
  "id": 1,
  "title": "Team Meeting at 3pm",
  "description": "Prepare presentation slides",
  "completed": false,
  "created_at": "2026-01-02T10:30:00Z",
  "updated_at": "2026-01-02T14:45:00Z"
}
```

**Validation Error Response** (400 Bad Request):
```json
{"error": "Title cannot be empty"}
{"error": "Title cannot exceed 200 characters"}
{"error": "Description cannot exceed 5000 characters"}
```

**Error Responses**:
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: Missing or invalid JWT token
- `404 Not Found`: Task doesn't exist OR task belongs to different user

**Notes**:
- `updated_at` is automatically refreshed server-side
- Omitted fields remain unchanged (partial updates supported)
- Cannot update `completed` status via this endpoint (use PATCH endpoint)
- Cannot change `user_id` or `id` (immutable)

---

### 5. Toggle Task Completion Status

**Endpoint**: `PATCH /api/tasks/{task_id}/toggle`

**Description**: Toggles task completion status (Pending ↔ Completed). Only succeeds if task belongs to authenticated user.

**Authentication**: Required (JWT)

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `task_id` | integer | Unique task identifier |

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Request Body**: None (toggle operation is idempotent based on current state)

**Success Response** (200 OK):
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2026-01-02T10:30:00Z",
  "updated_at": "2026-01-02T15:20:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT token
- `404 Not Found`: Task doesn't exist OR task belongs to different user

**Notes**:
- Operation is a toggle: `false → true` or `true → false`
- `updated_at` is automatically refreshed server-side
- No request body required (state is determined by current value)

---

### 6. Delete Task

**Endpoint**: `DELETE /api/tasks/{task_id}`

**Description**: Permanently deletes a task. Only succeeds if task belongs to authenticated user. Works for both pending and completed tasks.

**Authentication**: Required (JWT)

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `task_id` | integer | Unique task identifier |

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Request Body**: None

**Success Response** (204 No Content):
```
(Empty body)
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT token
- `404 Not Found`: Task doesn't exist OR task belongs to different user

**Notes**:
- Deletion is permanent (no soft delete or archive)
- Operation is idempotent (deleting non-existent task returns 404)
- No confirmation step (client should implement UI confirmation)

---

## Data Model Reference

### Task Entity

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-02T10:30:00Z",
  "updated_at": "2026-01-02T10:30:00Z"
}
```

**Field Descriptions**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | integer | Read-only, auto-increment | Unique task identifier |
| `title` | string | 1-200 chars, non-whitespace | Task title (required) |
| `description` | string \| null | 0-5000 chars | Task description (optional) |
| `completed` | boolean | `true` or `false` | Completion status |
| `created_at` | string (ISO 8601) | Read-only | Task creation timestamp (UTC) |
| `updated_at` | string (ISO 8601) | Auto-updated | Last modification timestamp (UTC) |

**Note**: `user_id` is not exposed in API responses (implicit from authentication context).

---

## Security Guarantees

1. **User Isolation**: All endpoints filter by `user_id` extracted from JWT token. No cross-user data access is possible.

2. **Ownership Validation**: Every mutating operation (PUT, PATCH, DELETE) verifies task ownership before execution.

3. **No User ID in URLs**: Task IDs are opaque integers. User context comes exclusively from JWT, preventing impersonation attacks.

4. **Input Validation**: All inputs are validated server-side (never trust client). Length limits and format checks enforced.

5. **SQL Injection Prevention**: SQLModel uses parameterized queries (ORM handles escaping).

6. **Error Message Security**: 404 errors are indistinguishable whether task doesn't exist or belongs to different user (prevents enumeration).

---

## Performance Considerations

- **Query Optimization**: All task queries use indexed `user_id` column for fast filtering
- **Response Size**: Task list endpoint optimized for up to 1000 tasks per user (< 2 second load time)
- **Database Connection Pooling**: Handled automatically by SQLModel async engine
- **No N+1 Queries**: Single query per endpoint (no lazy loading issues)

---

## Testing Checklist

- [ ] **Multi-User Isolation**: User A cannot access/modify User B's tasks (verified with 403/404)
- [ ] **Token Validation**: Expired/invalid tokens rejected with 401
- [ ] **Field Validation**: Title/description length limits enforced
- [ ] **Empty States**: Empty task list returns `[]` (not error)
- [ ] **Concurrency**: Simultaneous operations from multiple users succeed independently
- [ ] **Persistence**: Tasks survive server restarts
- [ ] **Error Handling**: Database failures return 500 with friendly message (no stack traces)

---

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-02 | 1.0.0 | Initial API contract based on approved specification |
