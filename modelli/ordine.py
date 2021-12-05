import datetime
import os

import stripe

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
    data_creazione = database.Column(database.DateTime, default=datetime.datetime.now)

    oggetti = database.relationship("OggettiNellOrdine", back_populates="ordine")

    @property
    def descrizione(self) -> str:
        """
        Genera una stringa rappresentante l'ordine composto da quantità e nomi degli oggetti
        """
        lista_stringhe = [
            f"- {ogg.quantita} x {ogg.oggetto.nome}" for ogg in self.oggetti
        ]
        return "\n".join(lista_stringhe)

    @property
    def importo(self) -> int:
        importo_oggetti = [ogg.oggetto.prezzo * ogg.quantita for ogg in self.oggetti]
        importo_centesimi = sum(importo_oggetti) * 100
        return int(importo_centesimi)

    def addebita_con_stripe(self, token: str) -> stripe.Charge:
        stripe.api_key = os.getenv("STRIPE_API_KEY")

        return stripe.Charge.create(
            amount=self.importo,  # in centesimi
            currency=os.getenv("VALUTA"),
            description=self.description,
            source=token,
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
