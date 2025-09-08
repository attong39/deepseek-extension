# 🔄 Migration Guide - ZETA AI Server

Instructions for upgrading between versions safely.

## 📋 Process

1) Read CHANGELOG for breaking changes
2) Create full backups (DB + files)
3) Stop services and ensure maintenance window
4) Apply DB migrations
5) Deploy new code
6) Run smoke tests and health checks
7) Monitor and rollback plan

## 🗃 Database Migrations

- Use Alembic: alembic upgrade head
- Check current/head revisions
- Zero-downtime patterns: expand/contract, roll-forward only

## 🧪 Post-Upgrade Checks

- /api/v1/health and detailed health
- Celery worker status
- Background jobs and schedules
- Data integrity checks

## 🧯 Rollback Strategy

- Keep previous image builds
- alembic downgrade to previous version if required
- Restore DB and file backups if necessary

## 🧭 References

- CHANGELOG.md
- DEPLOYMENT.md
- API Reference: ./API_REFERENCE.md

Last updated: 2025-08-14
