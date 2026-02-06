# weekdataback — Weekly Postgres backup in Docker

Overview
- Small project to run weekly backups of a Postgres database (default name `prod`) inside a Docker container using cron.

What I added
- `backup.sh` — single-file backup script that uses `pg_dump` and gzip.
- `backup.cron` — cron entry to run the script weekly (Sundays at 02:00).
- `Dockerfile` — Debian-based image with `postgresql-client` and `cron`.
- `docker-compose.yml` — convenience compose file to build and run the container.
- `.env.example` — environment variables example for DB credentials.
- `.gitignore` — ignore `backups/` (not checked in).

Environment variables
- `PGHOST` (required)
- `PGUSER` (required)
- `PGPASSWORD` (required)
- `PGDATABASE` (optional, default: `prod`)
- `PGPORT` (optional, default: `5432`)
- `BACKUP_DIR` (optional, default: `/backups`)
- `KEEP` (optional, number of backups to retain, default: `4`)
 - `S3_BUCKET` (optional) — if set, backups will be uploaded to this bucket
 - `S3_PATH` (optional) — prefix/path inside the bucket
 - `S3_DELETE_LOCAL_AFTER_UPLOAD` (optional, default `false`) — delete local file after successful upload
 - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION` (recommended as secrets)

Quick start (build & run via docker compose)

1. Copy `.env.example` to `.env` and fill DB credentials.

2. Build and start the container (from this folder):

```bash
docker compose up -d --build
```

3. Check logs:

```bash
docker logs -f weekdataback
```

Manual run (test backup immediately)

```bash
docker exec -it weekdataback /usr/local/bin/backup.sh
```

Docker secrets (no `.env`)

If you want to avoid using `.env`, create a local `secrets/` directory and put each value in a separate file named `PGHOST`, `PGUSER`, `PGPASSWORD`, and optionally `PGDATABASE`.

Example:

```bash
mkdir -p secrets
printf "db.example.host" > secrets/PGHOST
printf "dbuser" > secrets/PGUSER
printf "s3cr3tpass" > secrets/PGPASSWORD
printf "prod" > secrets/PGDATABASE
# AWS credentials for S3 upload (optional)
printf "AKIA..." > secrets/AWS_ACCESS_KEY_ID
printf "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" > secrets/AWS_SECRET_ACCESS_KEY
printf "us-east-1" > secrets/AWS_DEFAULT_REGION

To enable uploads to S3, set the `S3_BUCKET` environment variable in `docker-compose.yml` or pass it at runtime.
```

`docker compose` will mount these into the container at `/run/secrets/PGHOST`, etc. The container reads secrets first, then falls back to environment variables. Do NOT commit the `secrets/` directory.

Alternative: use Docker Swarm secrets or an external secrets manager for production-grade secret storage.

Backups location
- Host-mounted folder: `./backups` (created automatically by compose run).

Restore notes
- To restore a gzipped SQL dump: `gunzip -c file.sql.gz | psql -h host -U user -d targetdb`

Cron schedule
- Weekly on Sunday at 02:00 (container timezone)

Security notes
- Do not commit `.env` to source control. Use secrets manager or bind a read-only secret file.

Next steps
- Add S3/remote upload in `backup.sh` if you want off-host storage.
- Add health-check and alerting if backups fail.
