# python-app-01 — Working Notes

## Project
- FastAPI task CRUD API, PostgreSQL via RDS, EC2 t3.small (Ubuntu 22.04), us-east-1
- GitHub Actions CI/CD pipeline: lint → test → provision → configure → verify

## Decisions
- SQLite for tests (no RDS needed in CI); asyncpg for prod
- Alembic migrations run in configure stage BEFORE app starts
- db_host read from terraform output in configure stage (not threaded via job outputs — masked by GitHub secrets)
- db_password passed via -e to ansible-playbook (env var, no_log: true on tasks)
- venv at /opt/python-app-01/venv; systemd ExecStart uses absolute venv path
- EIP attached so IP is stable across instance stop/start

## Status
- [ ] Files generated
- [ ] validate_project passed
- [ ] Repo created
- [ ] DB_PASSWORD secret set
- [ ] Deployed
