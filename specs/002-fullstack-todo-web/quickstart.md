# Quickstart Guide: Multi-User Full-Stack Todo Web Application

**Feature**: 002-fullstack-todo-web
**Date**: 2026-01-02
**Purpose**: Get the development environment up and running in under 15 minutes

## Prerequisites

Before starting, ensure you have the following installed:

| Tool | Version | Check Command | Installation |
|------|---------|---------------|--------------|
| **Node.js** | 20.x or higher | `node --version` | [nodejs.org](https://nodejs.org/) |
| **npm** | 10.x or higher | `npm --version` | Included with Node.js |
| **Python** | 3.13 or higher | `python3 --version` | [python.org](https://www.python.org/) |
| **pip** | Latest | `pip3 --version` | Included with Python |
| **Git** | Any recent version | `git --version` | [git-scm.com](https://git-scm.com/) |

**Optional but Recommended**:
- **PostgreSQL Client** (`psql`) for database debugging
- **Postman** or **curl** for API testing

---

## Project Structure

```
todo-fullstack/
├── console/              # Phase I console app (reference only)
├── frontend/             # Next.js 16+ web application
│   ├── src/
│   │   ├── app/         # App Router pages
│   │   ├── components/  # React components
│   │   └── lib/         # Utilities
│   ├── .env.local       # Frontend environment variables (create this)
│   └── package.json
├── backend/              # FastAPI Python backend
│   ├── src/
│   │   ├── models/      # SQLModel database models
│   │   ├── api/         # FastAPI route handlers
│   │   └── auth/        # JWT validation logic
│   ├── tests/
│   ├── .env             # Backend environment variables (create this)
│   ├── requirements.txt
│   └── main.py
└── specs/                # Documentation (this directory)
```

---

## Step 1: Clone Repository

```bash
git clone <your-repo-url> todo-fullstack
cd todo-fullstack
git checkout 002-fullstack-todo-web  # Switch to feature branch
```

---

## Step 2: Database Setup (Neon PostgreSQL)

### Option A: Neon Serverless (Recommended)

1. **Create Neon Account**:
   - Go to [neon.tech](https://neon.tech)
   - Sign up for free account
   - Create new project: `todo-fullstack-dev`

2. **Get Connection String**:
   - Copy connection string from Neon dashboard
   - Format: `postgresql://user:password@host/dbname?sslmode=require`
   - **Important**: Replace `postgresql://` with `postgresql+asyncpg://` for SQLModel async support

3. **Example Connection String**:
   ```
   postgresql+asyncpg://alex:AbC123xyz@ep-cool-pond-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

### Option B: Local PostgreSQL

If you prefer local development:

```bash
# macOS (using Homebrew)
brew install postgresql@15
brew services start postgresql@15
createdb todo_dev

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
sudo -u postgres createdb todo_dev
```

**Local Connection String**:
```
postgresql+asyncpg://postgres:password@localhost:5432/todo_dev
```

---

## Step 3: Backend Setup (FastAPI)

```bash
cd backend

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env  # Or create manually (see below)
```

**Edit `backend/.env`**:
```bash
# JWT Secret (MUST match frontend - generate with: openssl rand -base64 32)
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-long

# Database URL (from Step 2)
DATABASE_URL=postgresql+asyncpg://user:pass@neon-host/dbname?sslmode=require

# CORS allowed origins (Next.js dev server)
CORS_ORIGINS=http://localhost:3000

# Optional: Enable SQL query logging
SQL_ECHO=true
```

**Verify Backend Setup**:
```bash
# Run database migrations (creates tables)
python -m src.init_db

# Start development server
uvicorn main:app --reload --port 8000

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete.
```

**Test Backend**:
```bash
# In another terminal
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "database": "connected"}
```

---

## Step 4: Frontend Setup (Next.js)

```bash
cd frontend  # From project root: cd ../frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local  # Or create manually (see below)
```

**Edit `frontend/.env.local`**:
```bash
# JWT Secret (MUST match backend - copy from backend/.env)
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-long

# Better Auth configuration
BETTER_AUTH_URL=http://localhost:3000

# Backend API URL (for server components)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Verify Frontend Setup**:
```bash
# Start development server
npm run dev

# Expected output:
# ▲ Next.js 16.0.0
# - Local:        http://localhost:3000
# ✓ Ready in 2.5s
```

**Test Frontend**:
- Open browser: http://localhost:3000
- You should see the sign-in page
- Check browser console for any errors

---

## Step 5: Full Stack Integration Test

With both servers running (backend on 8000, frontend on 3000):

### Test 1: Create Account

1. Navigate to http://localhost:3000/signup
2. Enter email: `test@example.com`
3. Enter password: `testpass123` (min 8 chars)
4. Click "Sign Up"
5. Should redirect to `/tasks` page (empty task list)

### Test 2: Create Task

1. On `/tasks` page, enter task title: "Test Task"
2. Enter description: "Verify full stack integration"
3. Click "Add Task"
4. Task should appear in list with "Pending" status

### Test 3: Toggle Completion

1. Click checkbox/toggle button on task
2. Task status should change to "Completed"
3. Visual indicator should update (e.g., strikethrough, color change)

### Test 4: Sign Out and Persistence

1. Click "Sign Out" button
2. Sign in again with same credentials
3. Task should still be visible (persistence verified)

### Test 5: Multi-User Isolation

1. Open incognito window: http://localhost:3000/signup
2. Create different account: `test2@example.com` / `testpass456`
3. Verify that `test2` sees empty task list (not `test` user's tasks)

---

## Common Issues & Solutions

### Issue: "Module not found: Can't resolve 'better-auth'"

**Solution**:
```bash
cd frontend
npm install better-auth
```

### Issue: "ModuleNotFoundError: No module named 'sqlmodel'"

**Solution**:
```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: Backend returns 401 for all requests

**Cause**: `BETTER_AUTH_SECRET` mismatch between frontend and backend

**Solution**:
1. Ensure both `.env` files use EXACT same secret
2. Restart both servers after changing `.env`
3. Clear browser cookies

### Issue: Database connection error

**Solution**:
```bash
# Verify connection string format
echo $DATABASE_URL  # Should start with postgresql+asyncpg://

# Test connection directly
psql <your-connection-string>
```

### Issue: CORS errors in browser console

**Cause**: Backend CORS middleware not configured correctly

**Solution**:
1. Verify `backend/.env` has `CORS_ORIGINS=http://localhost:3000`
2. Restart backend server
3. Clear browser cache

### Issue: "Password must be at least 8 characters" on valid password

**Cause**: Whitespace in password field

**Solution**: Ensure no leading/trailing spaces in password input

---

## Development Workflow

### Running Both Servers Concurrently

**Option A: Two Terminals**

Terminal 1:
```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload --port 8000
```

Terminal 2:
```bash
cd frontend
npm run dev
```

**Option B: Single Command (using `concurrently`)**

From project root:
```bash
npm install -g concurrently
concurrently "cd backend && .venv/bin/uvicorn main:app --reload" "cd frontend && npm run dev"
```

### Hot Reloading

- **Frontend**: Next.js auto-reloads on file changes (no restart needed)
- **Backend**: FastAPI `--reload` flag auto-reloads on `.py` file changes

### Stopping Servers

- Press `Ctrl+C` in each terminal
- Backend: Virtual environment remains active (deactivate with `deactivate`)

---

## Useful Development Commands

### Backend

```bash
# Activate virtual environment
source backend/.venv/bin/activate

# Run tests
pytest backend/tests/

# Run specific test file
pytest backend/tests/test_tasks_api.py

# Database migrations (when schema changes)
python -m src.init_db --reset  # WARNING: Deletes all data

# Open Python REPL with database access
python -m src.repl

# Format code
black backend/src/

# Type checking
mypy backend/src/
```

### Frontend

```bash
# Run tests
npm test

# Run tests in watch mode
npm test -- --watch

# Build for production
npm run build

# Type checking
npm run type-check

# Linting
npm run lint

# Format code
npm run format
```

---

## API Documentation

With backend running, access interactive API docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

**Try it out**:
1. Sign up via frontend to get a JWT token
2. Copy token from browser cookies (DevTools → Application → Cookies → `auth-token`)
3. In Swagger UI, click "Authorize" button
4. Enter: `Bearer <your-token>`
5. Test endpoints directly from browser

---

## Database Inspection

### Using `psql` (PostgreSQL CLI)

```bash
# Connect to database
psql <your-connection-string>

# Useful commands
\dt                    # List all tables
\d tasks               # Describe tasks table
\d users               # Describe users table

SELECT * FROM tasks;   # View all tasks
SELECT * FROM users;   # View all users (password hashes hidden)

# Check user isolation
SELECT user_id, COUNT(*) FROM tasks GROUP BY user_id;
```

### Using Neon Dashboard

1. Go to [console.neon.tech](https://console.neon.tech)
2. Select your project → "SQL Editor"
3. Run queries directly in browser

---

## Next Steps

Once your development environment is running:

1. **Read API Contracts**: `specs/002-fullstack-todo-web/contracts/tasks-api.md`
2. **Review Data Model**: `specs/002-fullstack-todo-web/data-model.md`
3. **Check Implementation Plan**: `specs/002-fullstack-todo-web/plan.md`
4. **Start with Phase 1**: Monorepo setup (see `tasks.md` when available)

---

## Environment Variables Reference

### Frontend `.env.local`

| Variable | Example | Description |
|----------|---------|-------------|
| `BETTER_AUTH_SECRET` | `abc123...` (32+ chars) | JWT signing secret (must match backend) |
| `BETTER_AUTH_URL` | `http://localhost:3000` | Frontend base URL |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Backend API URL |

### Backend `.env`

| Variable | Example | Description |
|----------|---------|-------------|
| `BETTER_AUTH_SECRET` | `abc123...` (32+ chars) | JWT validation secret (must match frontend) |
| `DATABASE_URL` | `postgresql+asyncpg://...` | Neon or local PostgreSQL connection string |
| `CORS_ORIGINS` | `http://localhost:3000` | Allowed CORS origins (comma-separated) |
| `SQL_ECHO` | `true` | Log SQL queries (optional, debug only) |

---

## Security Notes

- **Never commit `.env` files**: Both are in `.gitignore`
- **Rotate secrets in production**: Generate new `BETTER_AUTH_SECRET` for prod deployment
- **Use HTTPS in production**: HTTP is OK for local development only
- **Database connection strings contain credentials**: Never expose in logs or version control

---

## Support

- **Specification**: See `specs/002-fullstack-todo-web/spec.md`
- **API Contracts**: See `specs/002-fullstack-todo-web/contracts/`
- **Architecture Decisions**: See `history/adr/` (when created)
- **Troubleshooting**: Check browser console (frontend) and terminal logs (backend)

---

## Success Checklist

After completing this guide, you should be able to:

- [ ] Access frontend at http://localhost:3000 (sign-in page loads)
- [ ] Access backend health check at http://localhost:8000/health
- [ ] Create a new user account via signup page
- [ ] Sign in with created account
- [ ] Create a new task (appears in task list)
- [ ] Toggle task completion status
- [ ] Sign out and sign back in (task persists)
- [ ] Create second user account (sees empty task list - isolation verified)
- [ ] Access API docs at http://localhost:8000/docs

If all items are checked, your development environment is ready! 🎉

---

## Deployment Guide

### Frontend Deployment (Next.js)

#### Option 1: Vercel (Recommended)
1. Create account at [vercel.com](https://vercel.com)
2. Install Vercel CLI: `npm install -g vercel`
3. Navigate to frontend directory: `cd frontend`
4. Run deployment: `vercel`
5. Configure environment variables in Vercel dashboard:
   - `BETTER_AUTH_SECRET`: Same as backend
   - `NEXT_PUBLIC_API_URL`: Your production backend URL (e.g., `https://your-app.onrender.com`)

#### Option 2: Netlify
1. Create account at [netlify.com](https://netlify.com)
2. Navigate to frontend directory: `cd frontend`
3. Build for production: `npm run build`
4. Deploy via Netlify CLI or dashboard upload
5. Set environment variables in Netlify dashboard

#### Production Environment Variables (Frontend)
```
BETTER_AUTH_SECRET=your-production-secret
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
BETTER_AUTH_URL=https://your-frontend-domain.com
```

### Backend Deployment (FastAPI)

#### Option 1: Render (Recommended)
1. Create account at [render.com](https://render.com)
2. Create new Web Service
3. Connect to your GitHub repository
4. Set runtime: Python
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Configure environment variables:
   - `BETTER_AUTH_SECRET`: Same as frontend
   - `DATABASE_URL`: Production PostgreSQL connection string
   - `CORS_ORIGINS`: Your production frontend URL

#### Option 2: Railway
1. Create account at [railway.app](https://railway.app)
2. Import your repository
3. Select the backend directory
4. Set environment variables in Railway dashboard
5. Deploy automatically on git push

#### Production Environment Variables (Backend)
```
BETTER_AUTH_SECRET=your-production-secret
DATABASE_URL=postgresql+asyncpg://user:pass@prod-host/dbname
CORS_ORIGINS=https://your-frontend-domain.com
SQL_ECHO=false  # Disable in production
```

### Database Migration for Production

1. **Neon Production Branch**:
   - Create a production branch in your Neon dashboard
   - Use the production connection string in your environment variables

2. **Local PostgreSQL**:
   - Set up production database server
   - Update connection string accordingly

3. **Run Database Initialization**:
   ```bash
   # In production environment
   python -m src.init_db
   ```

### Environment-Specific Configuration

#### Development vs Production
| Environment | Frontend URL | Backend URL | Secrets |
|-------------|--------------|-------------|---------|
| Development | `http://localhost:3000` | `http://localhost:8000` | Local `.env` files |
| Production | `https://your-domain.com` | `https://your-backend.com` | Platform variables |

#### SSL/HTTPS Configuration
- **Frontend**: Enable HTTPS in hosting platform (Vercel/Netlify provide free SSL)
- **Backend**: Use platform's HTTPS termination or reverse proxy
- **Database**: Ensure `sslmode=require` in production connection strings

### Post-Deployment Checklist

- [ ] Frontend deployed and accessible via HTTPS
- [ ] Backend API deployed and accessible via HTTPS
- [ ] Environment variables correctly set in production
- [ ] Database connection established in production
- [ ] Authentication works end-to-end (signup → signin → tasks)
- [ ] Cross-origin requests work (frontend → backend)
- [ ] User isolation verified in production
- [ ] Health check passes: `GET /health`
- [ ] API documentation accessible: `GET /docs`

### Common Deployment Issues

#### CORS Errors in Production
- Verify `CORS_ORIGINS` includes your production domain
- Example: `https://your-app.vercel.app` (not `http://localhost`)

#### Database Connection Failures
- Check SSL mode in connection string
- Verify database is accessible from hosting platform
- Ensure database user has proper permissions

#### Authentication Failures
- Confirm `BETTER_AUTH_SECRET` is identical across platforms
- Check cookie security settings (secure: true for HTTPS)

---

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-02 | 1.0.0 | Initial quickstart guide for Phase II |
| 2026-01-03 | 1.0.1 | Added deployment guide for production environments |
