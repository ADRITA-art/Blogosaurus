# This file redirects to the app package to maintain compatibility
from app import create_app, db, migrate

# This allows imports like "from app import db" to work
# while still using the proper package structure
