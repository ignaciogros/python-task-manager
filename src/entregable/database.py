"""SQLAlchemy database instance."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared declarative base for all models."""


db = SQLAlchemy(model_class=Base)
