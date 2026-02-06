#!/usr/bin/env python3
"""
Command-line interface for the backup service.
"""
import argparse
import sys
from config import Config
from backup_service import run_backup
from scheduler import start_scheduler


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description='Database Backup and Export Service',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run a one-time backup
  python cli.py backup
  
  # Start scheduled backups
  python cli.py schedule
  
  # Show current configuration
  python cli.py config
        """
    )
    
    parser.add_argument(
        'command',
        choices=['backup', 'schedule', 'config'],
        help='Command to execute'
    )
    
    args = parser.parse_args()
    
    if args.command == 'backup':
        print("Starting database backup...")
        try:
            run_backup()
            print("Backup completed successfully!")
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'schedule':
        print("Starting scheduled backup service...")
        try:
            start_scheduler()
        except KeyboardInterrupt:
            print("\nScheduler stopped by user")
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'config':
        print("Current Configuration:")
        print(f"  Database Type: {Config.DB_TYPE}")
        print(f"  Database Host: {Config.DB_HOST}")
        print(f"  Database Port: {Config.DB_PORT}")
        print(f"  Database Name: {Config.DB_NAME}")
        print(f"  Database User: {Config.DB_USER}")
        print(f"  Backup Directory: {Config.BACKUP_DIR}")
        print(f"  Export Format: {Config.EXPORT_FORMAT}")
        print(f"  Scheduling Enabled: {Config.ENABLE_SCHEDULING}")
        if Config.ENABLE_SCHEDULING:
            print(f"  Scheduled Time: {Config.SCHEDULE_TIME}")


if __name__ == '__main__':
    main()
