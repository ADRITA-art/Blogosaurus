# This file redirects to the app package to maintain compatibility
from app import create_app, db, migrate

# Create an instance of the app for Gunicorn to use
app = create_app()

# This allows imports like "from app import db" to work
# while still using the proper package structure
