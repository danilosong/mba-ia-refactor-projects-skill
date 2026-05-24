from flask import Flask
from flask_cors import CORS

from src.config.settings import Settings
from src.database.connection import get_db
from src.middleware.error_handler import register_error_handlers
from src.routes.store_routes import bp as store_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = Settings.SECRET_KEY
    app.config["DEBUG"] = Settings.DEBUG
    CORS(app)
    app.register_blueprint(store_bp)
    register_error_handlers(app)
    get_db()
    return app
