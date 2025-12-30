---
id: 001
title: Project Constitution Setup
stage: constitution
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: junaidkh84
command: /sp.constitution
labels: ["constitution", "project-setup", "hackathon"]
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

/sp.contitution
Project: Phase I - Todo In-Memory Python Console App (Basic Level)

Core principles:
- Spec-driven development only (no manual coding allowed)
- Full transparency in process through detailed specs and iterations
- Clean, readable, and maintainable Python code
- Strict adherence to hackathon rules and deliverables
- Agentic workflow using Claude Code and Spec-Kit Plus exclusively

Key standards:
- Use Python 3.13+ with modern, idiomatic Python practices
- Proper project structure with /src folder for all source code
- All tasks stored in memory (list/dict-based, no files or databases)
- Task model must include: unique ID, title, description, status (pending/completed)
- Command-line interface must be intuitive and user-friendly
- Code must follow PEP 8 style guidelines
- Use type hints where appropriate
- Comprehensive error handling for invalid inputs

Constraints:
- Zero manual coding – all implementation via Claude Code generation
- All 5 basic features must be fully functional: Add, View, Update, Delete, Mark Complete
- No external dependencies beyond standard library (no third-party packages)
- Use UV for project management (virtual env and scripting)
- Console app must run without crashing on valid/invalid inputs

Deliverables (must be present in GitHub repo):
- Constitution file (this file)
- specs_history folder with all specification versions
- /src folder containing clean Python source code
- README.md with clear setup and run instructions
- CLAUDE.md documenting all prompts and iterations with Claude Code

Success criteria:
- Fully working console application demonstrating all 5 features
- Clear, iterative spec history showing thoughtful refinement
- Professional prompts and effective use of Claude Code
- Clean code structure with separation of concerns
- Smooth user experience in command-line interface
- All deliverables complete and well-organized

## Response snapshot

Constitution established for Phase I Todo Console App. Project configured for spec-driven development with Claude Code using Spec-Kit Plus workflow. All core principles, standards, constraints and deliverables documented in `.specify/memory/constitution.md`.

## Outcome

- ✅ Impact: Constitution file created; project foundations established
- 🧪 Tests: none (constitution phase)
- 📁 Files: `.specify/memory/constitution.md`
- 🔁 Next prompts: Run `/sp.specify` to create initial feature specification
- 🧠 Reflection: Constitution clearly defines hackathon requirements and agentic workflow constraints

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none (constitution phase)
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Create feature spec for todo app core functionality
