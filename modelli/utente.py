from flask import request, url_for
from requests import Response
from db.gestione import database
from libs.mailgun import invia_email


class ModelloUtente(database.Model):
    """Classe che rappresenta un utente dell'applicazione"""

    __tablename__ = "utenti"

    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(80), nullable=False, unique=True)
    email = database.Column(database.String(80), nullable=False, unique=True)
    password = database.Column(database.String(500), nullable=False)
    attivato = database.Column(database.Boolean, default=False)

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
        # request.url_root[:-1] = http://127.0.0.1:5000
        # url_for("confermautente", id_utente=self.id) = /conferma/<self.id>
        link = request.url_root[:-1] + url_for("confermautente", id_utente=self.id)
        soggetto = (
            "Conferma della registrazione all'applicazione REST Flask by Matteo Paolini"
        )
        testo = f"""
                Buongiorno,
                Per completare la registrazione vi preghiamo di visitare il seguente link: {link}.
                        
                Grazie!
                """
        html = f"""<html>Buongiorno,<br>
                Per completare la registrazione vi preghiamo di visitare <a href="{link}">il seguente link</a>.<br>
                <br>
                Grazie!</html>"""

        return invia_email([self.email], soggetto, testo, html)

    def salva(self):
        database.session.add(self)
        database.session.commit()

    def elimina(self):
        database.session.delete(self)
        database.session.commit()
