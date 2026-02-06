#!/usr/bin/env python3
"""
Configuration management for the backup service.
Loads environment variables and provides configuration settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for backup service."""
    
    # Database Configuration
    DB_TYPE = os.getenv('DB_TYPE', 'postgresql')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 5432))
    DB_NAME = os.getenv('DB_NAME', 'mydatabase')
    DB_USER = os.getenv('DB_USER', 'myuser')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'mypassword')
    
    # Backup Configuration
    BACKUP_DIR = os.getenv('BACKUP_DIR', './backups')
    EXPORT_FORMAT = os.getenv('EXPORT_FORMAT', 'json')
    SCHEDULE_TIME = os.getenv('SCHEDULE_TIME', '02:00')
    ENABLE_SCHEDULING = os.getenv('ENABLE_SCHEDULING', 'false').lower() == 'true'
    
    @classmethod
    def validate(cls):
        """Validate configuration settings."""
        valid_db_types = ['postgresql', 'mysql', 'mongodb']
        if cls.DB_TYPE not in valid_db_types:
            raise ValueError(f"DB_TYPE must be one of {valid_db_types}")
        
        valid_formats = ['json', 'csv', 'sql']
        if cls.EXPORT_FORMAT not in valid_formats:
            raise ValueError(f"EXPORT_FORMAT must be one of {valid_formats}")
        
        # Create backup directory if it doesn't exist
        os.makedirs(cls.BACKUP_DIR, exist_ok=True)
        
        return True
