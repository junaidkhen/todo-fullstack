---
id: 0001
title: Create Phase II Constitution
stage: constitution
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5
feature: none
branch: main
user: junaidkh84
command: /sp.constitution
labels: ["phase-2", "constitution", "full-stack", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

# Phase II Constitution - Todo Full-Stack Web Application

Create a new constitution file for Phase II in the repository root or /specs/phase2/ folder.

File path: /specs/phase2/constitution.md

Content must follow professional, concise format and cover Phase II specific principles.

Core Principles:
- Spec-driven development only (no manual coding)
- Monorepo structure with clear separation of frontend, backend, and console phases
- Multi-user isolation enforced at database and API level
- Authentication via Better Auth with JWT tokens (stateless)
- Persistent storage using Neon PostgreSQL via SQLModel
- Secure API: All endpoints require valid JWT, user ownership strictly enforced
- Clean architecture: separation of concerns in both frontend and backend
- Full transparency: all specs organized under /specs/ with proper referencing

Key Standards:
- Frontend: Next.js 16+ App Router, TypeScript, Tailwind CSS, server components preferred
- Backend: FastAPI, SQLModel, Pydantic models for requests/responses
- Database: tasks table with user_id foreign key, users managed by Better Auth
- API: RESTful endpoints under /api/tasks (no user_id in path), JWT in Authorization header
- Environment: Shared BETTER_AUTH_SECRET for JWT signing/verification
- Project structure: monorepo with /console (Phase I), /frontend, /backend, /specs
- Code quality: Type hints, PEP 8, proper error handling, meaningful responses

Constraints:
- Zero manual coding – all via Claude Code
- No external dependencies beyond specified stack
- All task operations filtered by authenticated user ID
- Data persistence across sessions
- Responsive frontend with intuitive UI for all 5 core features

Deliverables (in addition to working app):
- Updated monorepo structure
- Organized /specs/ folder with overview, architecture, features, api, database, ui specs
- Multiple CLAUDE.md files (root, frontend, backend)
- .spec-kit/config.yaml
- Complete prompt history in root CLAUDE.md or separate file

Success Criteria:
- Working full-stack app with signup/signin
- All 5 task features functional for multiple users with complete isolation
- Secure JWT-based authentication between frontend and backend
- Data persisted in PostgreSQL
- Clean, professional repository with all specs and documentation
- Smooth local development experience

Create this constitution file now and show me the content for approval before proceeding to monorepo restructuring and spec writing.

## Response snapshot

Created **separate phase-specific constitutions** (Option 2 per user preference):

**Phase I Constitution** (`specs/phase1/constitution.md` v1.0.0):
- Captured principles from completed console app
- 7 core principles: Simplicity First, Type Safety, TDD, Input Validation, In-Memory Storage, CLI, Clean Architecture
- Governs `/console` directory (formerly `Todo-app/`)
- Ratified: 2025-12-29, Amended: 2026-01-02

**Phase II Constitution** (`specs/phase2/constitution.md` v1.0.0):
- Establishes governance for full-stack web evolution
- 7 core principles: Spec-Driven Development, Multi-User Isolation, Clean Architecture, JWT Auth, Type Safety, Persistent Storage, RESTful API
- Governs `/frontend` and `/backend` directories
- Complete sections for technology stack, quality gates, deliverables, constraints
- Ratified: 2026-01-02

**Constitution Router** (`.specify/memory/constitution.md` v2.0.0):
- MAJOR version bump (restructured governance)
- Routes developers to appropriate phase constitution
- Defines universal principles (all phases)
- Provides phase summaries and compliance guidelines
- Includes monorepo structure documentation

All template files verified for compatibility.

## Outcome

- ✅ Impact: Established separate constitutional governance for Phase I (console) and Phase II (full-stack) with clear routing mechanism
- 🧪 Tests: none (governance documents)
- 📁 Files: specs/phase1/constitution.md, specs/phase2/constitution.md, .specify/memory/constitution.md (3 files created/updated)
- 🔁 Next prompts: User approval, then monorepo restructuring (move Todo-app → console) and Phase II spec creation
- 🧠 Reflection: Separate constitutions preserve Phase I history while enabling Phase II evolution with distinct architectural principles

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - all placeholders resolved, version properly set, templates verified
- Prompt variant (if applicable): standard /sp.constitution workflow
- Next experiment (smallest change to try): none - constitution creation successful
