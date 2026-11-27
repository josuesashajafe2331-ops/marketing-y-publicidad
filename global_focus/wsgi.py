# gunicorn wsgi:app   (la base de datos se inicializa al importar app.py)
from app import app  # noqa: F401
