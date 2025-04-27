from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
import os
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import app and db from your application
from app import app, db

# Initialize migration
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # Create a migration for the changes
        os.system('flask db migrate -m "Add created_at column to blog table"')
        # Apply the migration
        os.system('flask db upgrade')
        print("Migration completed successfully!")
