"""
Modulo per la gestione del DB mediante SQLAlchemy
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

convenzioni = {
    "ix": "idx_%(column_0_label)s",
    "uq": "unq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadati = MetaData(naming_convention=convenzioni)

database = SQLAlchemy(metadata=metadati)
