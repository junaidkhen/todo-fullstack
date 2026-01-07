# API Contract: Authentication API

**Feature**: 002-fullstack-todo-web
**Date**: 2026-01-02
**Purpose**: Authentication endpoints managed by Better Auth (Next.js)

## Overview

Authentication is handled entirely by **Better Auth** library running in the Next.js frontend. The FastAPI backend does NOT implement authentication endpoints—it only validates JWT tokens issued by Better Auth.

This document describes the Better Auth API surface that the frontend will use, for reference and integration testing purposes.

---

## Base URL

```
Development: http://localhost:3000/api/auth
Production: https://yourdomain.com/api/auth
```

**Implementation**: Better Auth plugin auto-generates these endpoints in Next.js App Router

---

## Endpoints Provided by Better Auth

### 1. User Registration (Signup)

**Endpoint**: `POST /api/auth/signup`

**Description**: Creates a new user account with email and password.

**Authentication**: Not required (public endpoint)

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "email": "alice@example.com",
  "password": "securepassword123"
}
```

**Request Schema**:
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `email` | string | Yes | Valid email format, unique | User's email address |
| `password` | string | Yes | Min 8 characters | User's password (will be bcrypt-hashed) |

**Success Response** (201 Created):
```json
{
  "user": {
    "id": "user-uuid-abc123",
    "email": "alice@example.com",
    "created_at": "2026-01-02T10:30:00Z"
  },
  "session": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresAt": "2026-01-03T10:30:00Z"
  }
}
```

**Validation Error Response** (400 Bad Request):
```json
{"error": "Invalid email format"}
{"error": "Password must be at least 8 characters"}
{"error": "Email already registered"}
```

**Notes**:
- Password is automatically hashed with bcrypt (12 rounds) before storage
- User is automatically signed in upon successful registration (session token returned)
- Session token is a JWT signed with `BETTER_AUTH_SECRET`

---

### 2. User Sign In (Login)

**Endpoint**: `POST /api/auth/signin`

**Description**: Authenticates user with email and password, returns session token.

**Authentication**: Not required (public endpoint)

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "email": "alice@example.com",
  "password": "securepassword123"
}
```

**Request Schema**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | User's email address |
| `password` | string | Yes | User's password |

**Success Response** (200 OK):
```json
{
  "user": {
    "id": "user-uuid-abc123",
    "email": "alice@example.com"
  },
  "session": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresAt": "2026-01-03T10:30:00Z"
  }
}
```

**Authentication Error Response** (401 Unauthorized):
```json
{"error": "Invalid email or password"}
```

**Notes**:
- Error message is intentionally vague (doesn't reveal whether email exists)
- Password is verified against bcrypt hash in database
- Session token is stored in HTTP-only cookie by Better Auth (automatic)

---

### 3. User Sign Out (Logout)

**Endpoint**: `POST /api/auth/signout`

**Description**: Invalidates current session and clears authentication cookie.

**Authentication**: Required (JWT token in cookie)

**Request Headers**:
```
Cookie: auth-token=<jwt_token>
```

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "success": true
}
```

**Notes**:
- Better Auth automatically clears the HTTP-only cookie
- Frontend should redirect to signin page after successful signout
- No error if user is already signed out (idempotent)

---

### 4. Get Current User Session

**Endpoint**: `GET /api/auth/session`

**Description**: Retrieves current authenticated user's session information.

**Authentication**: Required (JWT token in cookie)

**Request Headers**:
```
Cookie: auth-token=<jwt_token>
```

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "user": {
    "id": "user-uuid-abc123",
    "email": "alice@example.com"
  },
  "session": {
    "expiresAt": "2026-01-03T10:30:00Z"
  }
}
```

**Unauthenticated Response** (401 Unauthorized):
```json
{"error": "Not authenticated"}
```

**Notes**:
- Used by frontend to check if user is signed in
- Useful for route protection and conditional rendering

---

## JWT Token Structure

Better Auth generates JWT tokens with the following payload structure:

```json
{
  "sub": "user-uuid-abc123",
  "email": "alice@example.com",
  "iat": 1735819800,
  "exp": 1735906200
}
```

**Claims**:
| Claim | Description |
|-------|-------------|
| `sub` | User ID (UUID) - this is what FastAPI extracts as `user_id` |
| `email` | User's email address |
| `iat` | Issued at timestamp (Unix epoch) |
| `exp` | Expiration timestamp (Unix epoch) |

**Signing Algorithm**: HS256 (HMAC with SHA-256)
**Secret Key**: `BETTER_AUTH_SECRET` environment variable (must match in Next.js and FastAPI)

---

## Session Storage

Better Auth stores session tokens in **HTTP-only cookies** for security:

```
Cookie: auth-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Cookie Attributes**:
- `httpOnly: true` (prevents JavaScript access, mitigates XSS)
- `secure: true` (HTTPS only in production)
- `sameSite: lax` (CSRF protection)
- `path: /` (available across entire app)

**Frontend Integration**:
- Next.js server components can read cookie via `cookies().get('auth-token')?.value`
- Client components automatically include cookie in API requests
- FastAPI backend receives token in `Authorization: Bearer <token>` header (Next.js middleware adds this)

---

## FastAPI Integration (Backend Validation)

FastAPI does NOT implement these endpoints. It only validates tokens:

```python
from fastapi import Depends, HTTPException, Header
from jose import JWTError, jwt
import os

BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

async def get_current_user(authorization: str = Header(None)) -> str:
    """
    Dependency that validates JWT token and extracts user_id.
    Used in all protected FastAPI endpoints.
    """
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

**Usage in FastAPI Endpoints**:
```python
@app.get("/api/tasks")
async def list_tasks(current_user_id: str = Depends(get_current_user)):
    # current_user_id is guaranteed to be valid here
    tasks = await db.query(Task).filter(Task.user_id == current_user_id).all()
    return tasks
```

---

## Security Considerations

1. **Password Storage**: Bcrypt hashing with 12 rounds (handled by Better Auth)
2. **Token Security**: JWT signed with HS256 using shared secret
3. **Cookie Security**: HTTP-only, secure, SameSite=lax
4. **HTTPS**: Required for production deployment
5. **Token Expiration**: Default 24 hours (configurable in Better Auth)
6. **No Refresh Tokens**: MVP uses simple session expiration (can be added later)

---

## Frontend Integration Pattern

**Next.js Server Component** (fetching tasks with auth):
```typescript
// app/tasks/page.tsx
import { cookies } from 'next/headers';

export default async function TasksPage() {
  const token = cookies().get('auth-token')?.value;

  if (!token) {
    redirect('/signin');
  }

  const response = await fetch('http://localhost:8000/api/tasks', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (response.status === 401) {
    redirect('/signin');
  }

  const tasks = await response.json();
  return <TaskList tasks={tasks} />;
}
```

**Client Component** (sign in form):
```typescript
'use client';

export function SignInForm() {
  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    const response = await fetch('/api/auth/signin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: formData.get('email'),
        password: formData.get('password')
      })
    });

    if (response.ok) {
      router.push('/tasks'); // Redirect to task list
    } else {
      const error = await response.json();
      setError(error.error);
    }
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

---

## Environment Configuration

**Frontend (.env.local)**:
```bash
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend (.env)**:
```bash
BETTER_AUTH_SECRET=your-secret-key-min-32-chars  # MUST match frontend
DATABASE_URL=postgresql+asyncpg://user:pass@neon-host/dbname
CORS_ORIGINS=http://localhost:3000
```

**Critical Requirement**: `BETTER_AUTH_SECRET` MUST be identical in both frontend and backend for JWT validation to work.

---

## Token Expiration Handling

When JWT token expires during active session:

1. **Frontend Behavior** (from FR-036):
   - Preserve unsaved work in session storage
   - Redirect to `/signin` with message: "Your session expired. Please sign in again."
   - After successful re-authentication, restore unsaved work from session storage

2. **Backend Behavior**:
   - Return `401 Unauthorized` with `{"error": "Could not validate credentials"}`
   - Frontend intercepts 401 and initiates redirect flow

**Implementation Pattern** (Next.js middleware):
```typescript
// middleware.ts
export async function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')?.value;

  if (!token && isProtectedRoute(request.nextUrl.pathname)) {
    return NextResponse.redirect(new URL('/signin', request.url));
  }

  // Validate token expiration
  try {
    const payload = jwt.decode(token);
    if (payload.exp * 1000 < Date.now()) {
      // Token expired - redirect to signin
      return NextResponse.redirect(new URL('/signin?expired=true', request.url));
    }
  } catch (error) {
    return NextResponse.redirect(new URL('/signin', request.url));
  }

  return NextResponse.next();
}
```

---

## Testing Checklist

- [ ] **Registration**: New users can create accounts with valid email/password
- [ ] **Duplicate Email**: Registration fails with "Email already registered" for existing emails
- [ ] **Password Validation**: Registration fails with "Password must be at least 8 characters" for short passwords
- [ ] **Sign In Success**: Existing users can sign in with correct credentials
- [ ] **Sign In Failure**: Sign in fails with "Invalid email or password" for wrong credentials
- [ ] **Session Persistence**: Session cookie is set after successful signup/signin
- [ ] **Sign Out**: Sign out clears session cookie and user cannot access protected routes
- [ ] **JWT Validation**: FastAPI correctly extracts `user_id` from valid tokens
- [ ] **Expired Tokens**: FastAPI rejects expired tokens with 401
- [ ] **Invalid Tokens**: FastAPI rejects malformed/tampered tokens with 401
- [ ] **Secret Mismatch**: Tokens signed with different secret are rejected

---

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-02 | 1.0.0 | Initial auth contract documenting Better Auth integration |
