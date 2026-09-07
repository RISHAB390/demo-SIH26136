# AGENTS.md — Development Guidelines for SIH 26136

## Core Loop
Always follow the cycle:
PLAN → IMPLEMENT → RUN → TEST → FIX → VERIFY → COMMIT → NEXT MODULE

## Scope Guardrails
- Work module-by-module.
- Maintain exactly 9 database tables. No extra tables.
- Do NOT add out-of-scope libraries (Redis, Celery, JWT auth, WebSockets, AI/LLM models, external APIs).
- Maintain real PostgreSQL persistence.
- Keep decision support logic deterministic and explainable.
