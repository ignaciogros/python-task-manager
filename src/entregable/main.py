"""Flask application entry point."""
from dotenv import load_dotenv

load_dotenv()

from src.entregable import create_app

app = create_app()
