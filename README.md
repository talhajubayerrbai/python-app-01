# python-app-01

A FastAPI task management REST API backed by PostgreSQL, deployed on AWS EC2 with RDS.

## Architecture

```
Internet User → EC2 t3.small (:8000) → RDS PostgreSQL t3.micro
```

See `.udap/architecture.d2` for the full diagram.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{id}` | Get a task |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

Interactive docs available at `http://<host>:8000/docs` after deployment.

## Local Development

**Prerequisites:** Python 3.12, pip

```bash
# Create and activate virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run with SQLite (no database setup needed)
DATABASE_URL=sqlite+aiosqlite:///./dev.db uvicorn app.main:app --reload

# Run tests
pytest tests/ -v
```

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | SQLAlchemy async DB URL | Yes |

On the server, `.env` is written by Ansible from CI secrets.

## Deployment

Push to `main` — the pipeline runs automatically:

1. **lint** — flake8 on `app/`
2. **test** — pytest with SQLite
3. **provision** — Terraform: EC2 + RDS + security groups
4. **configure** — Ansible: Python env, app code, migrations, systemd service
5. **verify** — health check with retries

## CI Secrets

| Secret | Set by |
|--------|--------|
| `DB_PASSWORD` | You (via set_pipeline_secret before deploy) |
| `PROJECT_NAME` | Platform |
| `SSH_USER` / `SSH_PRIVATE_KEY` / `SSH_PUBLIC_KEY` | Platform |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` | Platform |
| `TF_STATE_BUCKET` | Platform |

## Operations

```bash
# SSH to the server
ssh -i <key> ubuntu@<instance_ip>

# View logs
sudo journalctl -u python-app-01 -f

# Restart service
sudo systemctl restart python-app-01

# Run migrations manually
cd /opt/python-app-01
source venv/bin/activate
DATABASE_URL=... alembic upgrade head
```

## Teardown

Use the **Destroy** action in the UDAP platform to tear down all AWS resources.
