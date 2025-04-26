from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()

load_dotenv()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Config")
    app.config.from_pyfile("config.py", silent=True)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .routes.auth_routes import auth_bp
    from .routes.blog_routes import blog_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    CORS(app, supports_credentials=True)

    with app.app_context():
        db.create_all()

    return app
