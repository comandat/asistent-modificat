# SKILL.md

Use this when setting up project infrastructure (Docker, CI/CD, Deployment).

## Decision Tree
Identify Project Type:
- **Node.js/TS**: Has `package.json`?
    - Yes -> Use `templates/node.Dockerfile` -> Create `Dockerfile`
    - Has `vitest`/`playwright`? -> Add CI steps to run tests.
- **Python**: Has `requirements.txt` / `pyproject.toml`?
    - Yes -> Use `templates/python.Dockerfile` -> Create `Dockerfile`
    - Has `pytest`? -> Add CI steps to run tests.
- **Static HTML**: Has `index.html` only?
    - Yes -> Use `nginx` image in Dockerfile.

## Execution Protocol
1. **Dockerize**:
   - Create `.dockerignore` (node_modules, venv, .git).
   - Create `Dockerfile` based on template.
   - Build & Test: `docker build -t app . && docker run --rm app`.

2. **CI/CD Pipeline (GitHub Actions)**:
   - Create `.github/workflows/ci.yml`.
   - Use `templates/ci.yml` as base.
   - Customize: Add `npm test` or `pytest` commands based on project tools.
   - Verify: Push to repo -> Check Actions tab.

3. **Orchestration (Optional)**:
   - If DB needed (Postgres/Redis) -> Create `docker-compose.yml`.
   - Link app service with DB service.
