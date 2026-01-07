# Phase II Constitution - Todo Full-Stack Web Application

## Core Principles

### I. Spec-Driven Development Only

All development MUST be driven by specifications. No manual coding is permitted outside of the spec → plan → tasks → implementation workflow. Every feature begins with a complete specification that defines requirements, acceptance criteria, and constraints before any implementation work begins.

**Rationale**: Ensures clear requirements, prevents scope creep, enables better planning, and maintains full traceability from user intent to implementation.

### II. Multi-User Isolation and Security

Multi-user isolation MUST be enforced at all layers: database (user_id foreign keys), API (JWT token validation), and business logic (ownership checks). All endpoints require valid JWT authentication. User data MUST never leak across user boundaries.

**Rationale**: Security is non-negotiable in multi-user applications. Defense in depth through layered isolation prevents accidental or malicious data exposure.

### III. Clean Architecture and Separation of Concerns

The codebase MUST maintain clear architectural boundaries:
- **Frontend**: Next.js 16+ App Router, TypeScript, Tailwind CSS, server components preferred
- **Backend**: FastAPI, SQLModel, Pydantic models for all requests/responses
- **Database**: Neon PostgreSQL via SQLModel ORM
- **Authentication**: Better Auth with stateless JWT tokens

Each layer has a single, well-defined responsibility. No layer may bypass or directly access another layer's internals.

**Rationale**: Clean architecture enables independent testing, easier maintenance, and clearer reasoning about system behavior.

### IV. Stateless JWT Authentication

Authentication MUST use Better Auth with JWT tokens. Tokens are stateless and validated on every request. Frontend and backend MUST share the same `BETTER_AUTH_SECRET` for token signing and verification. No session state is maintained on the server.

**Rationale**: Stateless authentication enables horizontal scaling, simplifies deployment, and reduces infrastructure complexity.

### V. Type Safety and Validation

All code MUST be fully typed:
- **Frontend**: TypeScript with strict mode enabled
- **Backend**: Python with type hints on all public functions and Pydantic models for all API contracts

All external inputs MUST be validated at system boundaries using Pydantic models.

**Rationale**: Type safety catches errors at development time, improves code quality, and enables better tooling support.

### VI. Persistent Storage with Clear Schema

All data MUST persist in Neon PostgreSQL. Database schema MUST include:
- `users` table managed by Better Auth
- `tasks` table with `user_id` foreign key enforcing referential integrity
- Proper indexes on frequently queried fields

No in-memory-only data structures for application state.

**Rationale**: Persistent storage ensures data durability across sessions. Well-designed schema with foreign keys prevents orphaned data and maintains referential integrity.

### VII. RESTful API Design

All backend endpoints MUST follow REST conventions:
- Resource-based URLs (e.g., `/api/tasks`, not `/api/get_tasks`)
- Standard HTTP methods (GET, POST, PUT, DELETE)
- JWT token in `Authorization: Bearer <token>` header
- No user_id in URL paths (extracted from validated JWT)
- Proper HTTP status codes (200, 201, 400, 401, 404, etc.)

**Rationale**: RESTful design provides predictable, standard interfaces that are easy to understand, test, and consume.

## Technology Stack Standards

### Frontend Requirements
- **Framework**: Next.js 16+ with App Router architecture
- **Language**: TypeScript with strict mode
- **Styling**: Tailwind CSS for all UI components
- **Rendering**: Server components preferred; client components only when interactivity required
- **API Integration**: Fetch API with proper error handling and loading states

### Backend Requirements
- **Framework**: FastAPI for high-performance async API
- **ORM**: SQLModel for type-safe database interactions
- **Validation**: Pydantic models for all request/response schemas
- **Database**: Neon PostgreSQL (serverless Postgres)
- **Authentication**: Better Auth for user management and JWT tokens

### Shared Standards
- **Environment Variables**: `.env` files for all secrets and configuration (never committed)
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Code Quality**: PEP 8 (Python), ESLint + Prettier (TypeScript)
- **Documentation**: All public APIs documented with examples

## Project Structure and Organization

### Monorepo Layout
```
/
├── console/           # Phase I in-memory console app (preserved)
├── frontend/          # Phase II Next.js application
├── backend/           # Phase II FastAPI application
├── specs/             # All specifications organized by feature
│   ├── phase1/        # Phase I specifications and constitution
│   └── phase2/        # Phase II specifications and constitution
├── history/           # Prompt history records and ADRs
├── .specify/          # SpecKit Plus templates and scripts
├── CLAUDE.md          # Root agent instructions
├── frontend/CLAUDE.md # Frontend-specific agent instructions
└── backend/CLAUDE.md  # Backend-specific agent instructions
```

### Specification Organization

All specs MUST reside under `/specs/phase2/` with clear naming and organization:
- `specs/phase2/constitution.md` - This file (governance and principles)
- `specs/phase2/overview.md` - High-level Phase II architecture
- `specs/phase2/architecture.md` - System design and component interaction
- `specs/phase2/features/*.md` - Individual feature specifications
- `specs/phase2/api.md` - Complete API contract documentation
- `specs/phase2/database.md` - Database schema and migrations
- `specs/phase2/ui.md` - UI/UX design and component specifications

All specifications MUST reference related specs, ADRs, and implementation artifacts.

## Development Workflow

### 1. Specification Phase
Every feature starts with a complete specification:
- Clear problem statement and user value
- Functional and non-functional requirements
- Acceptance criteria (testable conditions)
- API contracts with example requests/responses
- Database schema changes (if applicable)
- UI wireframes or component descriptions (frontend features)

### 2. Planning Phase
After spec approval, create a detailed implementation plan:
- Architecture decisions and rationale
- Component/module breakdown
- Integration points and dependencies
- Risk analysis and mitigation strategies
- Significant decisions captured as ADR suggestions

### 3. Task Breakdown
Convert plan into actionable, testable tasks:
- Each task has clear acceptance criteria
- Tasks are ordered by dependencies
- Each task can be completed and verified independently
- Test cases included where applicable

### 4. Implementation
Execute tasks following the plan:
- All changes must be small and testable
- Code references to modified files required
- No refactoring of unrelated code
- Security checks for common vulnerabilities (XSS, SQL injection, etc.)

### 5. Validation
Verify implementation against acceptance criteria:
- All tests passing
- Manual testing of user flows
- Security review for authentication/authorization changes
- Performance testing for database queries

## Quality Gates

### Code Quality Requirements
- **Type Coverage**: 100% type annotations on public APIs
- **Validation**: All external inputs validated with Pydantic models
- **Error Handling**: Proper error handling with meaningful messages
- **Documentation**: Public APIs documented with examples
- **Secrets Management**: No hardcoded secrets; all in `.env` files

### Testing Requirements
- **Unit Tests**: Core business logic must have unit test coverage
- **Integration Tests**: API endpoints tested with realistic scenarios
- **Manual Testing**: All user-facing features manually verified
- **Security Testing**: Authentication/authorization flows validated

### Security Requirements
- **Authentication**: All protected endpoints require valid JWT
- **Authorization**: User ownership verified on all data operations
- **Input Validation**: All user inputs validated and sanitized
- **SQL Injection**: Use parameterized queries (SQLModel handles this)
- **XSS Prevention**: Frontend properly escapes user-generated content

## Deliverables

### Working Application
- Multi-user signup and signin functionality
- All 5 core task features (add, list, mark complete, update, delete)
- Complete user isolation (users only see their own tasks)
- Persistent data storage in PostgreSQL
- Responsive, professional UI

### Documentation Artifacts
- Complete `/specs/phase2/` directory with all specifications
- Architecture Decision Records for significant choices
- Prompt History Records for all development sessions
- Updated README with setup and usage instructions
- API documentation with example requests/responses

### Project Configuration
- Root `CLAUDE.md` with general agent instructions
- `frontend/CLAUDE.md` with frontend-specific guidance
- `backend/CLAUDE.md` with backend-specific guidance
- `.spec-kit/config.yaml` (if applicable)
- Environment variable templates (`.env.example`)

## Constraints

### Non-Negotiable Constraints
- **Zero manual coding**: All code generated via Claude Code following spec → plan → tasks workflow
- **No additional dependencies**: Only use specified technology stack (Next.js, FastAPI, SQLModel, Better Auth, Neon)
- **Data persistence**: All user data must survive application restarts
- **Multi-user isolation**: Users must never see or modify other users' data
- **Responsive design**: UI must work on desktop and mobile browsers

### Development Constraints
- **Small changes**: Prefer multiple small, testable changes over large refactorings
- **No scope creep**: Implement only what is specified; suggest enhancements separately
- **Security first**: Never bypass authentication or authorization checks
- **Database migrations**: Schema changes must be versioned and repeatable

## Phase Transition from Phase I

### Preserved from Phase I
- Phase I console app code moved to `/console` directory
- Phase I specs and constitution under `specs/phase1/`
- Core 5 task features (add, list, update, delete, mark complete)
- Clean architecture principles
- Type safety requirements

### New in Phase II
- **Multi-user support**: User authentication and isolation
- **Persistence**: PostgreSQL database instead of in-memory storage
- **Web interface**: Next.js frontend instead of CLI
- **REST API**: FastAPI backend instead of command handlers
- **Stateless auth**: JWT tokens instead of single-user session

### Architectural Evolution
- **Storage**: In-memory lists → PostgreSQL database
- **Interface**: CLI REPL → Web UI + REST API
- **Users**: Single user → Multi-user with isolation
- **Auth**: None → Better Auth with JWT
- **Data model**: Python dataclass → SQLModel + Pydantic

## Governance

### Constitution Authority
This Phase II constitution supersedes all other development practices and guidelines. All specifications, plans, tasks, and implementations MUST comply with these principles. When conflicts arise, this document takes precedence.

### Amendment Process
Amendments to this constitution require:
1. Documented justification for the change
2. User approval of the proposed amendment
3. Version increment following semantic versioning:
   - **MAJOR**: Breaking changes to principles or removal of guarantees
   - **MINOR**: Addition of new principles or significant expansions
   - **PATCH**: Clarifications, wording improvements, non-semantic fixes
4. Update to all dependent templates and documentation
5. Communication of changes to all affected stakeholders

### Compliance and Review
- All pull requests MUST verify compliance with constitutional principles
- Complexity and deviation from standards MUST be justified with rationale
- Security requirements are non-negotiable and require explicit sign-off
- Performance standards must be validated with measurements, not assumptions

### Runtime Guidance
For day-to-day development guidance, consult the `CLAUDE.md` files at root, frontend, and backend levels. These files provide operational instructions that implement constitutional principles.

**Version**: 1.0.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-02
