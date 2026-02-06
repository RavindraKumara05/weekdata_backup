#!/usr/bin/env python3
"""
Export functionality for different file formats.
"""
import json
import csv
from datetime import datetime
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle special types."""
    
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


class Exporter:
    """Base class for data exporters."""
    
    def __init__(self, backup_dir):
        self.backup_dir = backup_dir
    
    def generate_filename(self, table_name, extension):
        """Generate filename with timestamp."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{self.backup_dir}/{table_name}_{timestamp}.{extension}"


class JSONExporter(Exporter):
    """Export data to JSON format."""
    
    def export(self, table_name, columns, data):
        """Export table data to JSON file."""
        filename = self.generate_filename(table_name, 'json')
        
        # Convert data to list of dictionaries
        records = []
        for row in data:
            record = {}
            for i, col in enumerate(columns):
                value = row[i]
                # Handle datetime objects
                if isinstance(value, datetime):
                    value = value.isoformat()
                record[col] = value
            records.append(record)
        
        with open(filename, 'w') as f:
            json.dump(records, f, indent=2, cls=JSONEncoder)
        
        return filename
    
    def export_mongodb(self, collection_name, documents):
        """Export MongoDB collection to JSON file."""
        filename = self.generate_filename(collection_name, 'json')
        
        with open(filename, 'w') as f:
            json.dump(documents, f, indent=2, cls=JSONEncoder)
        
        return filename


class CSVExporter(Exporter):
    """Export data to CSV format."""
    
    def export(self, table_name, columns, data):
        """Export table data to CSV file."""
        filename = self.generate_filename(table_name, 'csv')
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(columns)  # Write header
            writer.writerows(data)  # Write data
        
        return filename
    
    def export_mongodb(self, collection_name, documents):
        """Export MongoDB collection to CSV file."""
        filename = self.generate_filename(collection_name, 'csv')
        
        if not documents:
            return filename
        
        # Get all unique keys from documents
        keys = set()
        for doc in documents:
            keys.update(doc.keys())
        keys = sorted(list(keys))
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for doc in documents:
                # Convert ObjectId and datetime to strings
                row = {}
                for key in keys:
                    value = doc.get(key, '')
                    if isinstance(value, (ObjectId, datetime)):
                        value = str(value)
                    row[key] = value
                writer.writerow(row)
        
        return filename


class SQLExporter(Exporter):
    """Export data to SQL format."""
    
    def export(self, table_name, columns, data):
        """Export table data to SQL file."""
        filename = self.generate_filename(table_name, 'sql')
        
        with open(filename, 'w') as f:
            # Write CREATE TABLE statement (simplified)
            f.write(f"-- Backup of table: {table_name}\n")
            f.write(f"-- Created at: {datetime.now().isoformat()}\n\n")
            
            # Write INSERT statements
            for row in data:
                values = []
                for value in row:
                    if value is None:
                        values.append('NULL')
                    elif isinstance(value, (int, float)):
                        values.append(str(value))
                    elif isinstance(value, datetime):
                        values.append(f"'{value.isoformat()}'")
                    else:
                        # Escape single quotes
                        escaped = str(value).replace("'", "''")
                        values.append(f"'{escaped}'")
                
                columns_str = ', '.join(columns)
                values_str = ', '.join(values)
                f.write(f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});\n")
        
        return filename


def get_exporter(export_format, backup_dir):
    """Factory function to get appropriate exporter."""
    if export_format == 'json':
        return JSONExporter(backup_dir)
    elif export_format == 'csv':
        return CSVExporter(backup_dir)
    elif export_format == 'sql':
        return SQLExporter(backup_dir)
    else:
        raise ValueError(f"Unsupported export format: {export_format}")
