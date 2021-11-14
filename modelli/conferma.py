import os
from time import time
from uuid import uuid4

from db.gestione import database


class ModelloConferma(database.Model):
    __tablename__ = "conferme"
    id = database.Column(database.String(50), primary_key=True)
    scadenza = database.Column(database.Integer, nullable=False)
    confermata = database.Column(database.Boolean, nullable=False)
    id_utente = database.Column(
        database.Integer, database.ForeignKey("utenti.id"), nullable=False
    )
    utente = database.relationship("ModelloUtente", viewonly=True)

    def __init__(self, id_utente: int, **kwargs):
        super().__init__(**kwargs)
        self.id_utente = id_utente
        self.id = uuid4().hex
        self.scadenza = int(time()) + int(os.environ.get("DELTA_SCADENZA_CONFERMA"))
        self.confermata = False

    @classmethod
    def trova_per_id(cls, _id: str) -> "ModelloConferma":
        return cls.query.filter_by(id=_id).first()

    @property
    def e_scaduta(self) -> bool:
        return self.scadenza <= int(time())

    def porta_a_scadenza(self):
        if not self.e_scaduta:
            self.scadenza = int(time())
            self.salva()

    def salva(self):
        database.session.add(self)
        database.session.commit()

    def elimina(self):
        database.session.delete(self)
        database.session.commit()
