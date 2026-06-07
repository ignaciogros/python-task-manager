"""Flask application factory."""
import os

from flask import Flask

from src.entregable.database import db


def create_app(test_config: dict | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, template_folder="templates", static_folder="static")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from src.entregable.routes.user_stories import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
