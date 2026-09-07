# Architecture Specification — SIH 26136

## Monolithic Modular Architecture
The system is constructed as a clean modular monolith with:
- Single FastAPI backend application
- Single PostgreSQL database with exactly 9 application tables
- Single React + Vite frontend with role-specific dashboards and a demo persona selector

## Database Schema (Exactly 9 Tables)
1. `users`: id, name, role (`officer`, `startup`, `evaluator`), email
2. `startups`: id, user_id (FK `users.id`), name, sector, dpiit_status, profile_text
3. `challenges`: id, officer_id (FK `users.id`), title, description, outcomes, constraints, budget_band, required_sector, dpiit_required, status (`draft`, `published`, `closed`)
4. `applications`: id, startup_id (FK `startups.id`), challenge_id (FK `challenges.id`), proposal_text, status (`submitted`, `under_review`, `shortlisted`, `rejected`), UNIQUE(startup_id, challenge_id)
5. `evaluations`: id, application_id (FK `applications.id`, unique), evaluator_id (FK `users.id`), score (0-100), notes
6. `pilots`: id, application_id (FK `applications.id`, unique), scope, timeline_start, timeline_end, status (`planned`, `active`, `completed`, `extended`, `discontinued`), timeline_end >= timeline_start
7. `kpis`: id, pilot_id (FK `pilots.id`), name, target_value, unit
8. `evidence`: id, pilot_id (FK `pilots.id`), kpi_id (FK `kpis.id`), submitted_value, description, submitted_date, status (`pending`, `approved`, `rejected`), file_ref
9. `decisions`: id, pilot_id (FK `pilots.id`, unique), recommendation, notes

## Authorization Matrix
Authorization is enforced in backend middleware/dependency via the `X-User-Id` request header. The backend queries the real user record from the database and verifies permissions.
- Officer: Create Challenge, View Challenges, View Applications, Shortlist Application, Create Pilot, Define KPIs, Approve/Reject Evidence, View Decision Support, Record Final Decision
- Startup: View Challenges, Apply, View Own Applications, View Own Pilot & KPIs, Submit Evidence, View Own Decision Support
- Evaluator: View Challenges, View Applications, Submit Evaluation (0–100 score + notes)

## Decision Support Engine
Pure deterministic calculation:
$$\text{achievement\_ratio} = \frac{\text{approved\_kpis}}{\text{total\_kpis}}$$
- $\text{total\_kpis} = 0 \implies \text{"Insufficient Data"}$
- $\ge 0.70 \implies \text{"Recommend Scale"}$
- $0.40 \le \text{ratio} < 0.70 \implies \text{"Extend Pilot"}$
- $< 0.40 \implies \text{"Discontinue"}$
