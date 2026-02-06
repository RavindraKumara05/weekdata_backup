# Week Data Backup Service

A comprehensive database backup and export service that supports multiple database types and export formats. This service provides automated scheduled backups and on-demand backup capabilities for PostgreSQL, MySQL, and MongoDB databases.

## Features

- **Multi-Database Support**: PostgreSQL, MySQL, and MongoDB
- **Multiple Export Formats**: JSON, CSV, and SQL
- **Scheduled Backups**: Automated daily backups at configured times
- **On-Demand Backups**: Manual backup execution via CLI
- **Easy Configuration**: Environment-based configuration
- **Comprehensive Logging**: Detailed logging for monitoring and debugging

## Installation

1. Clone the repository:
```bash
git clone https://github.com/RavindraKumara05/weekdata_backup.git
cd weekdata_backup
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the service:
```bash
cp .env.example .env
# Edit .env with your database credentials and preferences
```

## Configuration

Edit the `.env` file to configure your database connection and backup settings:

```bash
# Database Configuration
DB_TYPE=postgresql          # Options: postgresql, mysql, mongodb
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydatabase
DB_USER=myuser
DB_PASSWORD=mypassword

# Backup Configuration
BACKUP_DIR=./backups        # Directory where backups will be stored
EXPORT_FORMAT=json          # Options: json, csv, sql
SCHEDULE_TIME=02:00         # Time for automated backups (24-hour format)
ENABLE_SCHEDULING=false     # Set to true for automated scheduled backups
```

## Usage

### Command Line Interface

The service provides a simple CLI with three main commands:

#### 1. Run a One-Time Backup
```bash
python cli.py backup
```

#### 2. Start Scheduled Backup Service
```bash
python cli.py schedule
```

#### 3. View Current Configuration
```bash
python cli.py config
```

### Programmatic Usage

You can also use the backup service programmatically:

```python
from backup_service import BackupService

# Create and run backup
service = BackupService()
service.backup_database()
```

## Supported Databases

### PostgreSQL
- Backs up all tables in the specified database
- Supports all PostgreSQL data types
- Export formats: JSON, CSV, SQL

### MySQL
- Backs up all tables in the specified database
- Supports all MySQL data types
- Export formats: JSON, CSV, SQL

### MongoDB
- Backs up all collections in the specified database
- Handles MongoDB-specific types (ObjectId, datetime)
- Export formats: JSON, CSV

## Export Formats

### JSON Format
- Human-readable JSON format
- Preserves data types
- Best for data interchange and API integration

### CSV Format
- Standard comma-separated values
- Compatible with spreadsheet applications
- Best for data analysis

### SQL Format
- SQL INSERT statements
- Can be directly imported into SQL databases
- Best for database restoration

## Directory Structure

```
weekdata_backup/
├── backup_service.py    # Core backup service
├── cli.py              # Command-line interface
├── config.py           # Configuration management
├── database.py         # Database connection handlers
├── exporters.py        # Export format handlers
├── scheduler.py        # Backup scheduler
├── requirements.txt    # Python dependencies
├── .env.example       # Example configuration file
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Backup Files

Backup files are stored in the configured `BACKUP_DIR` with timestamps:
- Format: `{table_name}_{timestamp}.{extension}`
- Example: `users_20260206_143022.json`

## Error Handling

The service includes comprehensive error handling:
- Connection failures are logged and reported
- Individual table/collection failures don't stop the entire backup
- Detailed error messages help with troubleshooting

## Logging

All operations are logged with timestamps:
- INFO: Normal operations and progress
- ERROR: Failures and exceptions
- Log format: `YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE`

## Security Considerations

1. **Protect your .env file**: Never commit it to version control
2. **Secure backup directory**: Ensure proper file permissions
3. **Use strong database credentials**: Follow your organization's security policies
4. **Regular backup verification**: Test restore procedures periodically

## Requirements

- Python 3.7+
- PostgreSQL (if backing up PostgreSQL databases)
- MySQL (if backing up MySQL databases)
- MongoDB (if backing up MongoDB databases)

## Dependencies

- `psycopg2-binary`: PostgreSQL adapter
- `pymysql`: MySQL adapter
- `pymongo`: MongoDB adapter
- `python-dotenv`: Environment variable management
- `schedule`: Task scheduling

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on GitHub.
