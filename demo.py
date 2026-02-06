#!/usr/bin/env python3
"""
Demo script showing how to use the backup service.
This creates a simple SQLite database for demonstration purposes.
"""
import sqlite3
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime


def create_demo_database():
    """Create a simple demo SQLite database."""
    db_path = '/tmp/demo_database.db'
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL,
            stock INTEGER
        )
    ''')
    
    # Insert sample data
    users_data = [
        (1, 'john_doe', 'john@example.com', '2026-01-01 10:00:00'),
        (2, 'jane_smith', 'jane@example.com', '2026-01-02 11:30:00'),
        (3, 'bob_wilson', 'bob@example.com', '2026-01-03 14:15:00'),
    ]
    
    products_data = [
        (1, 'Laptop', 999.99, 10),
        (2, 'Mouse', 29.99, 50),
        (3, 'Keyboard', 79.99, 30),
        (4, 'Monitor', 299.99, 15),
    ]
    
    cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', users_data)
    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?)', products_data)
    
    conn.commit()
    conn.close()
    
    print(f"Demo database created at: {db_path}")
    print(f"  - users table: {len(users_data)} rows")
    print(f"  - products table: {len(products_data)} rows")
    
    return db_path


def demo_backup_workflow():
    """Demonstrate the backup workflow."""
    print("\n" + "="*60)
    print("DATABASE BACKUP SERVICE - DEMO")
    print("="*60 + "\n")
    
    # Create demo database
    print("Step 1: Creating demo database...")
    db_path = create_demo_database()
    
    print("\nStep 2: Configuration")
    print("To use the backup service, you would:")
    print("  1. Copy .env.example to .env")
    print("  2. Configure your database credentials")
    print("  3. Choose export format (json, csv, or sql)")
    print("  4. Set backup directory")
    
    print("\nStep 3: Running backup")
    print("Command: python cli.py backup")
    print("  - Connects to your database")
    print("  - Extracts all tables/collections")
    print("  - Exports to chosen format")
    print("  - Saves with timestamp")
    
    print("\nStep 4: Scheduled backups (optional)")
    print("Command: python cli.py schedule")
    print("  - Runs backups at scheduled time")
    print("  - Continues running in background")
    print("  - Logs all operations")
    
    print("\n" + "="*60)
    print("EXAMPLE CONFIGURATION")
    print("="*60)
    print("""
# .env file example
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp_db
DB_USER=db_user
DB_PASSWORD=secure_password
BACKUP_DIR=./backups
EXPORT_FORMAT=json
SCHEDULE_TIME=02:00
ENABLE_SCHEDULING=true
    """)
    
    print("="*60)
    print("SUPPORTED DATABASES")
    print("="*60)
    print("✓ PostgreSQL - Full table backup")
    print("✓ MySQL - Full table backup")
    print("✓ MongoDB - Full collection backup")
    
    print("\n" + "="*60)
    print("EXPORT FORMATS")
    print("="*60)
    print("✓ JSON - Best for APIs and data interchange")
    print("✓ CSV - Best for Excel and data analysis")
    print("✓ SQL - Best for database restoration")
    
    print("\n" + "="*60)
    print("FILE NAMING")
    print("="*60)
    print(f"Example: users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    print(f"Example: products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    
    print("\n" + "="*60)
    print("For full documentation, see README.md")
    print("="*60 + "\n")


if __name__ == '__main__':
    demo_backup_workflow()
