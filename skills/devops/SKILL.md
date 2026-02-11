# SKILL.md

Use this to generate **production-ready** infrastructure (Docker, CI/CD, Deployment).
This skill ensures the application runs ANYWHERE, reliably.

## Philosophy
**Build Once, Run Everywhere.**
Security First. No secrets in Git.

## Decision Tree

### 1. START: Analyze Project
- **Language?**
  - Node.js (`package.json`) -> Use `templates/node.Dockerfile`.
  - Python (`requirements.txt`) -> Use `templates/python.Dockerfile`.
  - Go (`go.mod`) -> Use `templates/go.Dockerfile`.

### 2. EXECUTION: Generate Artifacts

#### A. Dockerization
1. **Security:** Create `.dockerignore` (exclude `node_modules`, `.env`, `.git`, `venv`).
2. **Efficiency:** Use **Multi-Stage Builds**.
   - Stage 1: Build (install deps, compile).
   - Stage 2: Runtime (copy artifacts, minimal image).
3. **Configuration:** Use `ENV` variables for dynamic config.
   - Create `.env.example` (template).
   - **NEVER** commit `.env` to Git.

#### B. CI/CD Pipeline (GitHub Actions)
1. **Create Workflow:** `.github/workflows/ci.yml`.
2. **Trigger:** `push` on `main`, `pull_request`.
3. **Steps:**
   - Checkout code.
   - Setup Environment (Node/Python).
   - Install Dependencies (Cache enabled).
   - Run Linter (`npm run lint`).
   - Run Tests (`npm test`).
   - Build (`npm run build`).

#### C. Orchestration (Docker Compose)
- Does the app need a Database?
  - Yes: Create `docker-compose.yml`.
  - Services: `app`, `db` (Postgres/Redis), `adminer` (optional).
  - Networking: Use `depends_on`.
  - Persistence: Use named volumes for DB data.

## Quality Standards
- **Healthcheck:** The Dockerfile MUST expose a port and include a `HEALTHCHECK` instruction or verify startup.
- **Minimal Size:** Use `alpine` or `slim` images.
- **Reproducible:** Pin versions (e.g., `node:20-alpine`, not `node:latest`).
