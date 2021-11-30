import os

from db.gestione import database
from modelli.oggetto import ModelloOggetto

relazione_ordini_oggetti = database.Table(
    "ordini_oggetti",
    database.Column("id_oggetto", database.Integer, database.ForeignKey("oggetti.id")),
    database.Column("id_ordine", database.Integer, database.ForeignKey("ordini.id")),
)


class ModelloOrdine(database.Model):
    __tablename__ = "ordini"

    id = database.Column(database.Integer, primary_key=True)
    stato = database.Column(database.String(20), nullable=False)

    oggetti = database.relationship(
        "ModelloOggetto", secondary=relazione_ordini_oggetti, lazy="dynamic"
    )

    @classmethod
    def trova_tutti(cls) -> list["ModelloOrdine"]:
        return cls.query.all()

    @classmethod
    def trova_per_id(cls, _id: int) -> "ModelloOrdine":
        return cls.query.filter_by(id=_id).first()

    def imposta_stato(self, nuovo_stato: str):
        self.stato = nuovo_stato
        self.salva()

    def salva(self):
        database.session.add(self)
        database.session.commit()

    def elimina(self):
        database.session.delete(self)
        database.session.commit()
