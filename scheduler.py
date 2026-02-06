#!/usr/bin/env python3
"""
Scheduler for automated backups.
Runs backups at scheduled times.
"""
import schedule
import time
import logging
from config import Config
from backup_service import run_backup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def scheduled_backup():
    """Function to be called by scheduler."""
    logger.info("Running scheduled backup")
    try:
        run_backup()
    except Exception as e:
        logger.error(f"Scheduled backup failed: {str(e)}")


def start_scheduler():
    """Start the backup scheduler."""
    if not Config.ENABLE_SCHEDULING:
        logger.info("Scheduling is disabled")
        return
    
    logger.info(f"Starting backup scheduler - backups will run at {Config.SCHEDULE_TIME}")
    schedule.every().day.at(Config.SCHEDULE_TIME).do(scheduled_backup)
    
    # Run initial backup immediately
    logger.info("Running initial backup")
    scheduled_backup()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == '__main__':
    start_scheduler()
