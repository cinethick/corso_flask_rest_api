import os

DEBUG = True
SECRET_KEY = os.environ["APP_SECRET_KEY"]
SESSION_TYPE = "filesystem"
SQLALCHEMY_DATABASE_URI = "sqlite:///db/dati.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
UPLOADED_IMMAGINI_DEST = os.path.join("static", "immagini")
JWT_BLOCKLIST_ENABLED = True
JWT_BLOCKLIST_TOKEN_CHECKS = ["access", "refresh"]
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
GITHUB = {
    "consumer_key": os.environ["GITHUB_CONSUMER_KEY"],
    "consumer_secret": os.environ["GITHUB_CONSUMER_SECRET"],
}
