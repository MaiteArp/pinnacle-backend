from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS # python: interpreter chose venv to resolve squiggly

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    # from app.models.ExampleModel import ExampleModel


    from app.models.user import User
    from app.models.session import Session
    from app.models.preference import Preference
    from app.models.challenge import Challenge
    

    db.init_app(app)
    migrate.init_app(app, db)
    # Register Blueprints here 
    from .routes import users_bp, sessions_bp, preferences_bp, challenges_bp, root_bp
    app.register_blueprint(users_bp)
    app.register_blueprint(sessions_bp)
    app.register_blueprint(preferences_bp)
    app.register_blueprint(challenges_bp)
    app.register_blueprint(root_bp)
    

    CORS(app)
    return app