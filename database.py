#!/usr/bin/env python3
"""
Database connection handlers for different database types.
"""
import psycopg2
import pymysql
from pymongo import MongoClient
from config import Config


class DatabaseConnection:
    """Factory class for creating database connections."""
    
    @staticmethod
    def get_connection(db_type=None):
        """Get appropriate database connection based on type."""
        db_type = db_type or Config.DB_TYPE
        
        if db_type == 'postgresql':
            return PostgreSQLConnection()
        elif db_type == 'mysql':
            return MySQLConnection()
        elif db_type == 'mongodb':
            return MongoDBConnection()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")


class PostgreSQLConnection:
    """PostgreSQL database connection handler."""
    
    def __init__(self):
        self.connection = None
        
    def connect(self):
        """Establish connection to PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD
            )
            return self.connection
        except Exception as e:
            raise Exception(f"Failed to connect to PostgreSQL: {str(e)}")
    
    def get_tables(self):
        """Get list of all tables in the database."""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return tables
    
    def get_table_data(self, table_name):
        """Get all data from a specific table."""
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        return columns, data
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()


class MySQLConnection:
    """MySQL database connection handler."""
    
    def __init__(self):
        self.connection = None
        
    def connect(self):
        """Establish connection to MySQL database."""
        try:
            self.connection = pymysql.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD
            )
            return self.connection
        except Exception as e:
            raise Exception(f"Failed to connect to MySQL: {str(e)}")
    
    def get_tables(self):
        """Get list of all tables in the database."""
        cursor = self.connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return tables
    
    def get_table_data(self, table_name):
        """Get all data from a specific table."""
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        return columns, data
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()


class MongoDBConnection:
    """MongoDB database connection handler."""
    
    def __init__(self):
        self.client = None
        self.db = None
        
    def connect(self):
        """Establish connection to MongoDB database."""
        try:
            connection_string = f"mongodb://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}"
            self.client = MongoClient(connection_string)
            self.db = self.client[Config.DB_NAME]
            # Test connection
            self.client.server_info()
            return self.db
        except Exception as e:
            raise Exception(f"Failed to connect to MongoDB: {str(e)}")
    
    def get_collections(self):
        """Get list of all collections in the database."""
        return self.db.list_collection_names()
    
    def get_collection_data(self, collection_name):
        """Get all documents from a specific collection."""
        collection = self.db[collection_name]
        documents = list(collection.find())
        return documents
    
    def close(self):
        """Close database connection."""
        if self.client:
            self.client.close()
