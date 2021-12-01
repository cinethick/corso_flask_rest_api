import os

from db.gestione import database


class OggettiNellOrdine(database.Model):
    __tablename__ = "ordini_oggetti"

    id = database.Column(database.Integer, primary_key=True)
    id_oggetto = database.Column(database.Integer, database.ForeignKey("oggetti.id"))
    id_ordine = database.Column(database.Integer, database.ForeignKey("ordini.id"))
    quantita = database.Column(database.Integer)

    oggetto = database.relationship("ModelloOggetto")
    ordine = database.relationship("ModelloOrdine", back_populates="oggetti")


class ModelloOrdine(database.Model):
    __tablename__ = "ordini"

    id = database.Column(database.Integer, primary_key=True)
    stato = database.Column(database.String(20), nullable=False)

    oggetti = database.relationship("OggettiNellOrdine", back_populates="ordine")

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
