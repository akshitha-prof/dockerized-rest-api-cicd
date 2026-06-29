# Dockerized REST API with CI/CD Pipeline

A production-style **Task Manager REST API** built with FastAPI, containerized with Docker, and shipped via a GitHub Actions CI/CD pipeline. Designed to demonstrate cloud deployment, containerization, automated testing, and software delivery best practices.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI + SQLAlchemy |
| Database | PostgreSQL (Docker) / SQLite (tests) |
| Containerization | Docker + docker-compose |
| CI/CD | GitHub Actions |
| Testing | pytest + pytest-cov |
| Cloud Deployment | AWS EC2 / GCP Compute Engine (Ubuntu) |

---

## Architecture

```
┌─────────────────────────────────────┐
│         GitHub Actions CI/CD         │
│  push → test → build → push image   │
└────────────────┬────────────────────┘
                 │
         ┌───────▼────────┐
         │   Docker Hub   │
         │  (image store) │
         └───────┬────────┘
                 │
    ┌────────────▼─────────────┐
    │     AWS EC2 / GCP VM     │  ← Ubuntu, port 8000 open
    │  ┌────────┐ ┌──────────┐ │
    │  │  API   │ │ Postgres │ │  ← docker-compose
    │  │:8000   │ │  :5432   │ │
    │  └────────┘ └──────────┘ │
    └──────────────────────────┘
```

---

## Quick Start (Local)

```bash
# Clone
git clone https://github.com/akshitha-prof/dockerized-rest-api-cicd.git
cd dockerized-rest-api-cicd

# Run with Docker Compose (API + PostgreSQL)
docker-compose up --build

# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List all tasks (filter by `?completed=true/false`) |
| GET | `/tasks/{id}` | Get a single task |
| PATCH | `/tasks/{id}` | Update task fields |
| DELETE | `/tasks/{id}` | Delete a task |

---

## Running Tests

```bash
pip install -r requirements.txt
pytest tests/ -v --cov=app --cov-report=term-missing
```

18 test cases covering happy paths, edge cases, and 404 handling.

---

## CI/CD Pipeline

On every push to `main`:
1. **Test job** — installs dependencies, runs full pytest suite with coverage
2. **Docker build job** (runs only if tests pass) — builds the image, pushes to Docker Hub tagged with `latest` and the commit SHA

See [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml) for the full pipeline definition.

---

## Cloud Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions to deploy on **AWS EC2** or **GCP Compute Engine**, including security group / firewall configuration and networking concepts.
