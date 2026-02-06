#!/usr/bin/env python3
"""
Core backup service module.
Handles backup operations for different database types.
"""
import logging
from datetime import datetime
from config import Config
from database import DatabaseConnection
from exporters import get_exporter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BackupService:
    """Main backup service class."""
    
    def __init__(self):
        """Initialize backup service."""
        Config.validate()
        self.db_connection = None
        self.exporter = get_exporter(Config.EXPORT_FORMAT, Config.BACKUP_DIR)
    
    def backup_database(self):
        """Perform full database backup."""
        logger.info(f"Starting backup for {Config.DB_TYPE} database: {Config.DB_NAME}")
        start_time = datetime.now()
        
        try:
            # Get database connection
            self.db_connection = DatabaseConnection.get_connection()
            self.db_connection.connect()
            logger.info("Database connection established")
            
            if Config.DB_TYPE == 'mongodb':
                self._backup_mongodb()
            else:
                self._backup_sql_database()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(f"Backup completed successfully in {duration:.2f} seconds")
            
        except Exception as e:
            logger.error(f"Backup failed: {str(e)}")
            raise
        finally:
            if self.db_connection:
                self.db_connection.close()
                logger.info("Database connection closed")
    
    def _backup_sql_database(self):
        """Backup SQL database (PostgreSQL or MySQL)."""
        tables = self.db_connection.get_tables()
        logger.info(f"Found {len(tables)} tables to backup")
        
        backed_up_files = []
        for table in tables:
            try:
                logger.info(f"Backing up table: {table}")
                columns, data = self.db_connection.get_table_data(table)
                filename = self.exporter.export(table, columns, data)
                backed_up_files.append(filename)
                logger.info(f"Table {table} backed up to {filename} ({len(data)} rows)")
            except Exception as e:
                logger.error(f"Failed to backup table {table}: {str(e)}")
        
        logger.info(f"Backed up {len(backed_up_files)} tables")
        return backed_up_files
    
    def _backup_mongodb(self):
        """Backup MongoDB database."""
        collections = self.db_connection.get_collections()
        logger.info(f"Found {len(collections)} collections to backup")
        
        backed_up_files = []
        for collection in collections:
            try:
                logger.info(f"Backing up collection: {collection}")
                documents = self.db_connection.get_collection_data(collection)
                
                if Config.EXPORT_FORMAT == 'json':
                    filename = self.exporter.export_mongodb(collection, documents)
                elif Config.EXPORT_FORMAT == 'csv':
                    filename = self.exporter.export_mongodb(collection, documents)
                else:
                    logger.warning(f"SQL export not supported for MongoDB, using JSON instead")
                    json_exporter = get_exporter('json', Config.BACKUP_DIR)
                    filename = json_exporter.export_mongodb(collection, documents)
                
                backed_up_files.append(filename)
                logger.info(f"Collection {collection} backed up to {filename} ({len(documents)} documents)")
            except Exception as e:
                logger.error(f"Failed to backup collection {collection}: {str(e)}")
        
        logger.info(f"Backed up {len(backed_up_files)} collections")
        return backed_up_files


def run_backup():
    """Run backup operation."""
    try:
        service = BackupService()
        service.backup_database()
    except Exception as e:
        logger.error(f"Backup operation failed: {str(e)}")
        raise


if __name__ == '__main__':
    run_backup()
