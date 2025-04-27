import os
import sys
import sqlite3
from sqlalchemy import inspect
from app import db

# Database path - adjust if needed
db_path = "instance/blogosaurus.db"  # Update this with your actual database path

def add_column_raw_sqlite():
    try:
        # Connect directly to SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(blog)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'created_at' not in columns:
            cursor.execute('ALTER TABLE blog ADD COLUMN created_at TIMESTAMP')
            print("Added created_at column to blog table successfully")
        else:
            print("created_at column already exists")
            
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting database migration...")
    add_column_raw_sqlite()
    print("Database migration completed")
