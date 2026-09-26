# 🚀 Team Setup Guide — ProcureBridge (SIH 26136)

Get the full stack running on your machine in under 10 minutes.

---

## Prerequisites

| Tool | Version |
|------|---------|
| Git | any |
| Python | 3.11 or 3.12 (not 3.14+) |
| Node.js | 20.x or later |
| Docker Desktop | any (for the database) |

---

## Step 1 — Clone the repository

```bash
git clone https://github.com/<your-org>/demo-SIH26136.git
cd demo-SIH26136
```

---

## Step 2 — Start PostgreSQL (Docker)

```bash
docker compose -f docker-compose.dev.yml up -d
```

This starts only the database on port **5432**. It uses these credentials by default:
- User: `postgres`
- Password: `mysecretpassword`
- Database: `sih_db`

> **No Docker?** Install PostgreSQL 15 locally, create a database called `sih_db`, and note your credentials.

---

## Step 3 — Backend Setup

```bash
cd backend

# Create Python virtual environment
python -m venv .venv

# Activate it
# Windows:
.\.venv\Scripts\activate
# Mac / Linux:
source .venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Create your `.env` file

> ⚠️ **Windows users:** Do NOT use `echo '...' > .env` in PowerShell — it creates a broken UTF-16 file.
> Instead, copy the example file:

```bash
# Mac/Linux:
cp .env.example .env

# Windows:
copy .env.example .env
```

Open `backend/.env` in any editor (VS Code, Notepad++) and update if needed:
```env
DATABASE_URL=postgresql+psycopg://postgres:mysecretpassword@localhost:5432/sih_db
APP_ENV=development
JWT_SECRET_KEY=my-local-dev-secret
```

### Run database migrations and start the server

```bash
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

The API is now at **http://localhost:8000** — check `/docs` for the interactive Swagger UI.

> **Optional:** Seed demo data with `python seed.py`

---

## Step 4 — Frontend Setup

Open a **new terminal** (keep backend running):

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
# Windows:
copy .env.example .env
# Mac/Linux:
cp .env.example .env
```

The default `frontend/.env` contains:
```env
VITE_API_URL=http://localhost:8000
```

Start the dev server:
```bash
npm run dev
```

The app is now at **http://localhost:5173**

---

## Test Accounts (after running seed.py)

| Role | Email | Password |
|------|-------|----------|
| Startup | contact@aquasense.io | demo123 |
| Officer | priya.nair@waterboard.gov.in | demo123 |
| Evaluator | rahul.verma@techboard.gov.in | demo123 |

---

## Running Tests

```bash
cd backend
# Activate venv first!
python -m pytest
```

Tests use SQLite in-memory by default (no PostgreSQL needed for CI).

---

## Full Docker Deployment (Production)

```bash
# Create a .env at the project root with your secrets:
cp .env.example .env  # (edit POSTGRES_PASSWORD, JWT_SECRET_KEY, CORS_ORIGINS)

# Build and start everything
docker compose up --build -d

# App is served at http://localhost (port 80)
```

Create `.env` at the **project root** (not inside backend/):
```env
POSTGRES_PASSWORD=yourStrongPasswordHere
JWT_SECRET_KEY=yourRandomSecretAtLeast32CharsLong!
CORS_ORIGINS=http://localhost,https://yourdomain.com
```

---

## Common Problems & Fixes

| Problem | Fix |
|---------|-----|
| `DATABASE_URL field required` | Your `backend/.env` is missing or has wrong encoding. Re-copy from `.env.example` |
| `connection refused port 5432` | Run `docker compose -f docker-compose.dev.yml up -d` to start PostgreSQL |
| `alembic: command not found` | Your venv is not activated. Run `.\.venv\Scripts\activate` (Windows) |
| `npm run dev` gives 401 / 404 | Check `frontend/.env` has `VITE_API_URL=http://localhost:8000` and backend is running |
| `pytest fails with Settings error` | Tests need `DATABASE_URL` set — this is set automatically in CI via env vars |
| `uploads/ missing` | The directory is tracked via `.gitkeep` — if gone, create it: `mkdir backend/uploads` |
