from flask import request, url_for
from requests import Response

from db.gestione import database
from libs.mailgun import invia_email
from libs.testi import prendi_testo
from modelli.conferma import ModelloConferma


class ModelloUtente(database.Model):
    """Classe che rappresenta un utente dell'applicazione"""

    __tablename__ = "utenti"

    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(80), nullable=False, unique=True)
    email = database.Column(database.String(80), unique=True)
    password = database.Column(database.String(500))

    conferme = database.relationship(
        "ModelloConferma", lazy="dynamic", cascade="all, delete-orphan"
    )

    @property
    def conferma_piu_recente(self) -> "ModelloConferma":
        return self.conferme.order_by(database.desc(ModelloConferma.scadenza)).first()

    @classmethod
    def trova_per_nome(cls, nome: str) -> "ModelloUtente":
        return cls.query.filter_by(nome=nome).first()

    @classmethod
    def trova_per_email(cls, email: str) -> "ModelloUtente":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def trova_per_id(cls, _id: int) -> "ModelloUtente":
        return cls.query.filter_by(id=_id).first()

    def invia_conferma_email(self) -> Response:
        link = request.url_root[:-1] + url_for(
            "conferma", id_conferma=self.conferma_piu_recente.id
        )
        soggetto = prendi_testo("conferma_email_soggetto")
        testo = prendi_testo("conferma_email_testo").format(link)
        html = prendi_testo("conferma_email_html").format(link)

        return invia_email([self.email], soggetto, testo, html)

    def salva(self):
        database.session.add(self)
        database.session.commit()

    def elimina(self):
        database.session.delete(self)
        database.session.commit()
