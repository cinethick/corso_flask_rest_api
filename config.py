import os

DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite://db/dati.db")
