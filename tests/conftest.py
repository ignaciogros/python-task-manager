"""Shared pytest fixtures."""
import pytest
from sqlalchemy.pool import StaticPool

from src.entregable import create_app
from src.entregable.database import db as _db


@pytest.fixture
def app():
    """Flask app backed by an in-memory SQLite database."""
    flask_app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_ENGINE_OPTIONS": {
            "connect_args": {"check_same_thread": False},
            "poolclass": StaticPool,
        },
        "SECRET_KEY": "test-secret",
    })
    yield flask_app
    with flask_app.app_context():
        _db.drop_all()


@pytest.fixture
def client(app):
    """Flask test client."""
    with app.test_client() as c:
        yield c
