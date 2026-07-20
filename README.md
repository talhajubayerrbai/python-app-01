# python-app-01

A FastAPI task management REST API (todos domain) deployed on AWS EC2 behind an Application Load Balancer, backed by PostgreSQL on RDS.

## Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI 0.115 + Uvicorn |
| Database | PostgreSQL 17 (RDS t3.micro) |
| ORM | SQLAlchemy 2 (async) + Alembic |
| Server | EC2 t3.small (Ubuntu 22.04) |
| Load Balancer | AWS ALB (internet-facing, HTTP :80) |
| Region | us-east-1 |
| CI/CD | GitHub Actions |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/todos` | List all items |
| POST | `/todos` | Create an item |
| GET | `/todos/{id}` | Get an item by ID |
| PUT | `/todos/{id}` | Update an item |
| DELETE | `/todos/{id}` | Delete an item |

The ALB DNS name is printed in the verify stage log after each deploy. The Swagger UI is available at `/docs` on the ALB hostname.

## Item Schema

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

## Local Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

# Run tests (SQLite, no RDS required)
pytest tests/ -v

# Run the app locally
DATABASE_URL=sqlite+aiosqlite:///./dev.db uvicorn app.main:app --reload
```

## Deployment

Triggered via GitHub Actions on push to `main`.

Pipeline: lint -> test -> provision -> configure -> verify

- **provision**: Terraform creates the EC2 instance, ALB, and RDS database
- **configure**: Ansible deploys the app, runs Alembic migrations, starts the systemd service
- **verify**: Polls the ALB health endpoint until the app responds

## Network Layout

```
Internet -> ALB :80 -> EC2 :8000 -> RDS :5432
```

Security groups:
- ALB: inbound :80 from the internet
- EC2: inbound :22 from the internet, inbound :8000 from the ALB security group only
- RDS: inbound :5432 from the EC2 security group only
