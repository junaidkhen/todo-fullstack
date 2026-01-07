# Multi-User Full-Stack Todo Web Application

A modern, full-stack todo list application with user authentication, persistent storage, and responsive web interface. Built with Next.js, FastAPI, and PostgreSQL for production-ready task management.

## Features

- ✅ **Multi-User Authentication** - Secure sign-up and sign-in with Better Auth
- ✅ **Task Management** - Create, view, update, complete, and delete tasks
- ✅ **User Isolation** - Strict data separation between users (no cross-user access)
- ✅ **Persistent Storage** - Tasks stored in Neon PostgreSQL database
- ✅ **Responsive UI** - Works on mobile, tablet, and desktop devices
- ✅ **Real-time Updates** - Optimistic UI with loading states and error handling
- ✅ **JWT Authentication** - Stateless authentication with token validation

## Requirements

- **Frontend**: Node.js 20.x+, npm 10.x+
- **Backend**: Python 3.13+, pip
- **Database**: PostgreSQL (local or Neon serverless)
- **Development**: Git

## Quick Setup

### Prerequisites

1. **Install Node.js and npm** (version 20.x+)
2. **Install Python 3.13+** with pip
3. **Install Git**

### Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url> todo-fullstack
   cd todo-fullstack
   ```

2. **Set up the backend (FastAPI)**:
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Create backend environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set:
   ```bash
   # Generate a secure secret: openssl rand -base64 32
   BETTER_AUTH_SECRET=your-32-char-secret-here
   DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/todo_dev
   CORS_ORIGINS=http://localhost:3000
   ```

4. **Set up the frontend (Next.js)**:
   ```bash
   cd ../frontend
   npm install
   cp .env.example .env.local
   ```

   Edit `.env.local` and set:
   ```bash
   BETTER_AUTH_SECRET=your-32-char-secret-here  # Same as backend
   BETTER_AUTH_URL=http://localhost:3000
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

5. **Initialize the database**:
   ```bash
   cd ../backend
   python -m src.init_db
   ```

6. **Start both servers** (in separate terminals):
   ```bash
   # Terminal 1 - Backend
   cd backend
   source .venv/bin/activate
   uvicorn main:app --reload --port 8000

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

7. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Backend API Docs: http://localhost:8000/docs

## Project Structure

```
todo-fullstack/
├── console/              # Phase I console app (reference only)
├── frontend/             # Next.js 16+ web application
│   ├── src/
│   │   ├── app/         # App Router pages (signup, signin, tasks)
│   │   ├── components/  # React components (TaskList, TaskForm, etc.)
│   │   └── lib/         # Utilities (auth, api)
│   ├── public/          # Static assets
│   ├── package.json
│   └── .env.local       # Frontend environment variables
├── backend/              # FastAPI Python backend
│   ├── src/
│   │   ├── models/      # SQLModel database models
│   │   ├── api/         # FastAPI route handlers
│   │   ├── auth/        # JWT validation logic
│   │   └── database.py  # Database connection management
│   ├── tests/           # Backend tests
│   ├── main.py          # FastAPI app entry point
│   ├── requirements.txt
│   └── .env             # Backend environment variables
├── specs/                # Documentation and specifications
└── README.md             # This file
```

## Running Tests

### Backend Tests
```bash
cd backend
source .venv/bin/activate
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Environment Variables

### Backend (.env)
- `BETTER_AUTH_SECRET`: JWT signing secret (must match frontend)
- `DATABASE_URL`: PostgreSQL connection string (with asyncpg)
- `CORS_ORIGINS`: Comma-separated list of allowed origins

### Frontend (.env.local)
- `BETTER_AUTH_SECRET`: JWT validation secret (must match backend)
- `NEXT_PUBLIC_API_URL`: Backend API URL for server components

## API Endpoints

### Authentication (via Better Auth)
- `POST /api/auth/signup` - Create new user
- `POST /api/auth/signin` - Sign in existing user
- `POST /api/auth/signout` - Sign out user

### Task Management
- `GET /api/tasks` - List user's tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `PATCH /api/tasks/{id}/toggle` - Toggle completion status
- `DELETE /api/tasks/{id}` - Delete task

## Development

### Code Quality
- **Frontend**: TypeScript strict mode, ESLint, Prettier
- **Backend**: Python type hints, Black formatting, mypy
- **Testing**: Pytest for backend, Jest for frontend
- **Security**: JWT validation, SQL injection prevention

### Adding New Features
1. Update data models in `backend/src/models/` if needed
2. Add API endpoints in `backend/src/api/`
3. Create React components in `frontend/src/components/`
4. Update Next.js pages in `frontend/src/app/`
5. Write tests in respective test directories
6. Update documentation

## Deployment

### Frontend (Next.js)
1. Build for production: `npm run build`
2. Deploy to Vercel, Netlify, or similar platform
3. Set environment variables in deployment platform

### Backend (FastAPI)
1. Build Docker container or deploy directly
2. Set production environment variables
3. Use production PostgreSQL instance
4. Configure SSL/HTTPS

## Security Features

- **JWT Authentication**: Stateless, secure token-based auth
- **User Isolation**: Each user can only access their own tasks
- **SQL Injection Prevention**: SQLModel parameterized queries
- **CORS Configuration**: Restricted to allowed origins only
- **Password Security**: Better Auth handles secure password hashing

## Troubleshooting

**Q: Frontend can't connect to backend**
- Check that both servers are running
- Verify CORS settings in backend `.env`
- Ensure `NEXT_PUBLIC_API_URL` matches backend address

**Q: Authentication fails between frontend and backend**
- Verify `BETTER_AUTH_SECRET` is identical in both `.env` files
- Restart both servers after changing secrets
- Clear browser cookies and cache

**Q: Database connection errors**
- Check PostgreSQL is running and accessible
- Verify `DATABASE_URL` format: `postgresql+asyncpg://...`
- Test connection with `psql` directly

**Q: Task data not persisting**
- Verify database initialization was successful
- Check that `python -m src.init_db` ran without errors
- Confirm database connection string is correct

## Contributing

This project follows Spec-Driven Development practices. To contribute:
1. Review the specifications in `specs/002-fullstack-todo-web/`
2. Follow the implementation plan in `specs/002-fullstack-todo-web/plan.md`
3. Add tests for new functionality
4. Update documentation as needed

## License

This project was created as part of a coding exercise. Feel free to use and modify as needed.

## Credits

Built with:
- **Frontend**: Next.js 16+, React, TypeScript, Tailwind CSS, Better Auth
- **Backend**: FastAPI, Python 3.13+, SQLModel, asyncpg
- **Database**: PostgreSQL (Neon serverless)
- **Development**: Following Spec-Driven Development methodology
"# todo" 
"# todo-fullstack" 
