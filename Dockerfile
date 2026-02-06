FROM debian:12-slim

RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    postgresql-client \
    cron \
    ca-certificates \
    gzip \
    awscli \
  && rm -rf /var/lib/apt/lists/*

COPY backup.sh /usr/local/bin/backup.sh
RUN chmod +x /usr/local/bin/backup.sh

COPY backup.cron /etc/cron.d/backup-cron
RUN chmod 0644 /etc/cron.d/backup-cron \
  && crontab /etc/cron.d/backup-cron

RUN mkdir -p /backups /var/log && touch /var/log/backup.log
VOLUME ["/backups"]

EXPOSE 80
CMD ["cron", "-f"]
