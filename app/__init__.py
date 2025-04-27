# Proper Flask application initialization
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
jwt = JWTManager()

def fix_render_postgres_url(url):
    """Fix PostgreSQL URL for Render.com format if needed."""
    if not url:
        return url
    
    if 'postgresql://' in url and '@dpg-' in url and '.oregon-postgres.render.com' not in url:
        pattern = r'@(dpg-[^/]+)'
        match = re.search(pattern, url)
        if match:
            host = match.group(1)
            corrected_host = f"{host}.oregon-postgres.render.com"
            url = url.replace(f"@{host}", f"@{corrected_host}")
            print(f"Fixed PostgreSQL URL: {url}")
    
    return url

def create_app(config=None):
    app = Flask(__name__)
    
    # Configure app
    app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # Adjust as needed
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'  # Replace with a secure key
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Test database connection
    with app.app_context():
        try:
            # For SQLAlchemy 2.x compatibility
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            db.session.commit()
            print('Database connection successful!')

            db.create_all()
            print('Tables created!')
        except Exception as e:
            print(f"Database connection error: {e}")
    
    # Register blueprints
    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    
    # Register blog blueprint
    from .routes.blog_routes import blog_bp
    app.register_blueprint(blog_bp)
    
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))
    
    # Register routes - will add later
    @app.route('/')
    def home():
        return 'Flask application is running successfully!'
    
    return app
