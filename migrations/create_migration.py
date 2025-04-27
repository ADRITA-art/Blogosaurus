from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import sys

# Path to your app directory
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, app_dir)

def create_migration_app():
    # Create a minimal Flask application for migrations
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app_dir, 'instance', 'blogosaurus.db')
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    database = SQLAlchemy(flask_app)
    
    # Import models to ensure they're registered
    from app.models import User, Blog
    
    # Initialize migrations
    migrate = Migrate(flask_app, database)
    
    return flask_app, database, migrate

if __name__ == '__main__':
    app, db, migrate = create_migration_app()
    with app.app_context():
        db.create_all()
        
        # Check if column exists and add it if needed
        inspector = db.inspect(db.engine)
        columns = [column['name'] for column in inspector.get_columns('blog')]
        
        if 'created_at' not in columns:
            try:
                db.engine.execute('ALTER TABLE blog ADD COLUMN created_at DATETIME')
                print("Added created_at column to blog table successfully")
            except Exception as e:
                print(f"Error adding column: {e}")
        else:
            print("created_at column already exists")
            
    print("Migration process completed!")
