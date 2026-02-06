#!/usr/bin/env bash
set -euo pipefail

# Minimal single-file Postgres backup script for database 'prod' (default)
# Expects DB credentials via environment variables or .env passed to Docker:
#   PGHOST, PGPORT (optional, default 5432), PGUSER, PGPASSWORD, PGDATABASE (default: prod)
# Optional: BACKUP_DIR (default /backups), KEEP (number of backups to keep, default 4)

## Support reading credentials from Docker secrets (/run/secrets/) or environment variables.
for v in PGHOST PGUSER PGPASSWORD PGDATABASE PGPORT BACKUP_DIR KEEP; do
  if [ -f "/run/secrets/$v" ]; then
    export "$v"="$(cat "/run/secrets/$v")"
  fi
done

# Defaults
PGDATABASE="${PGDATABASE:-prod}"
PGPORT="${PGPORT:-5432}"
BACKUP_DIR="${BACKUP_DIR:-/backups}"
KEEP="${KEEP:-4}"

# Validate required values
if [ -z "${PGHOST:-}" ] || [ -z "${PGUSER:-}" ] || [ -z "${PGPASSWORD:-}" ]; then
  echo "[backup] ERROR: PGHOST, PGUSER and PGPASSWORD are required via /run/secrets or environment"
  exit 1
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="${BACKUP_DIR}/${PGDATABASE}_backup_${TIMESTAMP}.sql.gz"

mkdir -p "$BACKUP_DIR"
export PGPASSWORD="$PGPASSWORD"

echo "[backup] starting backup for database '$PGDATABASE' to $FILENAME"
pg_dump -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" "$PGDATABASE" | gzip > "$FILENAME"
echo "[backup] finished: $FILENAME"

# rotate: keep only the most recent $KEEP backups
if command -v ls >/dev/null 2>&1; then
  echo "[backup] pruning older backups, keeping $KEEP"
  ls -1t "$BACKUP_DIR/${PGDATABASE}_backup_"*.sql.gz 2>/dev/null | tail -n +$((KEEP+1)) | xargs -r rm --
fi

echo "[backup] done"

# --- optional S3 upload ---
# Read AWS creds/secrets if present
for v in AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_DEFAULT_REGION S3_BUCKET S3_PATH S3_DELETE_LOCAL_AFTER_UPLOAD; do
  if [ -f "/run/secrets/$v" ]; then
    export "$v"="$(cat "/run/secrets/$v")"
  fi
done

S3_PATH="${S3_PATH:-}"            # optional prefix inside bucket
S3_DELETE_LOCAL_AFTER_UPLOAD="${S3_DELETE_LOCAL_AFTER_UPLOAD:-false}"

if [ -n "${S3_BUCKET:-}" ]; then
  if ! command -v aws >/dev/null 2>&1; then
    echo "[backup] WARNING: aws CLI not found; skipping S3 upload"
  else
    echo "[backup] uploading $FILENAME to s3://$S3_BUCKET/${S3_PATH}"
    aws s3 cp "$FILENAME" "s3://$S3_BUCKET/${S3_PATH}$(basename "$FILENAME")"
    if [ $? -eq 0 ]; then
      echo "[backup] uploaded to S3: s3://$S3_BUCKET/${S3_PATH}$(basename "$FILENAME")"
      if [ "${S3_DELETE_LOCAL_AFTER_UPLOAD,,}" = "true" ]; then
        echo "[backup] deleting local file $FILENAME"
        rm -f "$FILENAME"
      fi
    else
      echo "[backup] ERROR uploading to S3"
    fi
  fi
fi
