"""
Simple Database Table Viewer - View all SQLite tables and their data
"""

import sqlite3
import json
from pathlib import Path

DB_PATH = "./test.db"

class DatabaseViewer:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
    
    def connect(self):
        """Connect to database"""
        if not Path(self.db_path).exists():
            print(f"Database file not found: {self.db_path}")
            return False
        
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            print(f"[OK] Connected to database: {self.db_path}")
            return True
        except Exception as e:
            print(f"[ERROR] Connection error: {e}")
            return False
    
    def get_all_tables(self):
        """Get list of all tables"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        return sorted(tables)
    
    def get_table_info(self, table_name):
        """Get table schema information"""
        cursor = self.connection.cursor()
        cursor.execute(f"PRAGMA table_info(`{table_name}`)")
        columns = cursor.fetchall()
        return columns
    
    def get_table_data(self, table_name, limit=100):
        """Get table data"""
        cursor = self.connection.cursor()
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
        row_count = cursor.fetchone()[0]
        
        # Get data
        cursor.execute(f"SELECT * FROM `{table_name}` LIMIT {limit}")
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        return columns, rows, row_count
    
    def print_table_schema(self, table_name):
        """Print table schema"""
        try:
            columns = self.get_table_info(table_name)
            
            print(f"\n{'='*120}")
            print(f"TABLE: {table_name}")
            print(f"{'='*120}")
            print(f"{'Column Name':<30} {'Type':<20} {'PK':<5} {'NOT NULL':<12} {'Default':<20}")
            print(f"{'-'*30} {'-'*20} {'-'*5} {'-'*12} {'-'*20}")
            
            for col in columns:
                col_id, col_name, col_type, notnull, dflt_value, pk = col
                pk_str = "Yes" if pk else "No"
                notnull_str = "Yes" if notnull else "No"
                dflt_str = str(dflt_value) if dflt_value else "-"
                print(f"{col_name:<30} {col_type:<20} {pk_str:<5} {notnull_str:<12} {dflt_str:<20}")
        except Exception as e:
            print(f"[ERROR] Error reading schema for {table_name}: {e}")
    
    def print_table_data(self, table_name, limit=50):
        """Print table data"""
        try:
            columns, rows, row_count = self.get_table_data(table_name, limit)
            
            print(f"\nData ({min(len(rows), limit)} of {row_count} rows):")
            print(f"{'-'*120}")
            
            if not rows:
                print("  [Empty table]")
                return
            
            # Print header
            header = " | ".join([f"{col:<15}" for col in columns])
            print(header)
            print(f"{'-'*120}")
            
            # Print rows
            for row in rows:
                values = []
                for col in columns:
                    val = row[col]
                    if val is None:
                        val_str = "NULL"
                    elif isinstance(val, str):
                        val_str = val[:15] if len(val) > 15 else val
                    else:
                        val_str = str(val)[:15]
                    values.append(f"{val_str:<15}")
                print(" | ".join(values))
        except Exception as e:
            print(f"[WARN] Error reading data for {table_name}: {e}")
    
    def show_all_tables(self):
        """Show schema and data for all tables"""
        tables = self.get_all_tables()
        
        if not tables:
            print("[ERROR] No tables found in database")
            return
        
        print("\n" + "="*120)
        print(f"DATABASE TABLES ({len(tables)} tables)")
        print("="*120)
        
        # List all tables
        for i, table in enumerate(tables, 1):
            try:
                cursor = self.connection.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
                count = cursor.fetchone()[0]
                print(f"{i:2}. {table:<35} ({count:5} rows)")
            except Exception as e:
                print(f"{i:2}. {table:<35} [ERROR: {str(e)[:40]}]")
        
        print("\n" + "="*120 + "\n")
        
        # Show each table
        for table in tables:
            try:
                self.print_table_schema(table)
                self.print_table_data(table, limit=20)
            except Exception as e:
                print(f"\n[WARN] Error processing table {table}: {e}")
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("\n[OK] Database connection closed")


if __name__ == "__main__":
    viewer = DatabaseViewer(DB_PATH)
    
    if viewer.connect():
        try:
            viewer.show_all_tables()
        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            viewer.close()
    else:
        print("\n[INFO] Database will be created on first API request")
        print("   The database file should appear at: ./test.db")
