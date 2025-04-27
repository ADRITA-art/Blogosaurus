from app import create_app, db
from app.models import User, Blog
from sqlalchemy import inspect

# Create the Flask application
app = create_app()

# Push an application context
with app.app_context():
    print("Database connection successful!")
    print("Creating database tables...")
    db.create_all()
    print("Database tables created successfully!")
    
    # Optionally, add a test user
    test_user = User.query.filter_by(email='test@example.com').first()
    if not test_user:
        from werkzeug.security import generate_password_hash
        test_user = User(
            username='testuser',
            email='test@example.com',
            password=generate_password_hash('password123')
        )
        db.session.add(test_user)
        db.session.commit()
        print("Test user created.")
    else:
        print("Test user already exists.")

    # List all tables to confirm creation
    inspector = inspect(db.engine)
    print("Created tables:", inspector.get_table_names())
