import os
import sys
from flask_migrate import Migrate
from sqlalchemy import text

# Add the parent directory to the path if needed
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the Flask application and database
from app import create_app, db
from app.models import Blog, User

# Create the app with the appropriate configuration
app = create_app()

# Initialize migrations
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        
        # Check if the created_at column exists
        inspector = db.inspect(db.engine)
        columns = [column['name'] for column in inspector.get_columns('blog')]
        
        if 'created_at' not in columns:
            try:
                # Add column using SQLAlchemy 2.0 compatible method
                db.session.execute(text('ALTER TABLE blog ADD COLUMN created_at DATETIME'))
                db.session.commit()
                print("Added created_at column to blog table successfully")
            except Exception as e:
                print(f"Error adding created_at column: {e}")
        else:
            print("created_at column already exists in blog table")
            
        print("Database schema update process completed!")
