from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    #app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("RENDER_DATABASE_URI")

    # Import models here for Alembic setup
    # from app.models.ExampleModel import ExampleModel
    from .models.board import Board
    from .models.card import Card

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from app.routes.board_routes import board_bp
    from app.routes.card_routes import card_bp
    app.register_blueprint(board_bp)
    app.register_blueprint(card_bp)


    CORS(app)
    return app
