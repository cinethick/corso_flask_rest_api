import os
import traceback
from time import time

from flask import make_response, render_template, Response
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource

from libs.mailgun import MailGunException
from libs.testi import prendi_testo
from modelli.conferma import ModelloConferma
from modelli.utente import ModelloUtente
from schemi.conferma import SchemaConferma

schema_conferma = SchemaConferma()


class Conferma(Resource):
    @classmethod
    def get(cls, id_conferma: str):
        conferma = ModelloConferma.trova_per_id(id_conferma)

        if not conferma:
            return {"errore": prendi_testo("conferma_non_trovata")}, 404

        if conferma.confermata:
            return {"errore": prendi_testo("conferma_gia_attivata")}, 400

        if conferma.e_scaduta:
            return {"errore": prendi_testo("conferma_scaduta")}, 400

        try:
            conferma.confermata = True
            conferma.porta_a_scadenza()  # salva
        except:
            return {"errore": prendi_testo("conferma_modificazione")}, 500

        return Response(
            "conferma.html",
            titolo=os.getenv("MAILGUN_TITOLO") + " - Conferma account Utente",
            email=conferma.utente.email,
        )


class ConfermaUtente(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def get(cls, id_utente: int):
        claims = get_jwt()
        if not claims["admin"]:
            return {
                "errore": prendi_testo("non_autorizzato"),
                "suggerimento": prendi_testo("conferma_suggerimento"),
            }, 401

        utente = ModelloUtente.trova_per_id(id_utente)

        if not utente:
            return {"errore": prendi_testo("utente_non_trovato").format(id_utente)}, 404

        return (
            {
                "tempo_corrente": int(time()),
                "conferma": [
                    schema_conferma.dump(conferma)
                    for conferma in utente.conferme.order_by(ModelloConferma.scadenza)
                ],
            },
            200,
        )

    @classmethod
    def post(cls, id_utente: int):
        utente = ModelloUtente.trova_per_id(id_utente)

        if not utente:
            return {"errore": prendi_testo("utente_non_trovato").format(id_utente)}, 404

        try:
            conferma = utente.conferma_piu_recente

            if conferma:
                if conferma.confermata:
                    return {"errore": prendi_testo("conferma_gia_attivata")}, 400
                conferma.porta_a_scadenza()

            nuova_conferma = ModelloConferma(id_utente)
            nuova_conferma.salva()
            utente.invia_conferma_email()
            return {"messaggio": prendi_testo("conferma_inserito")}, 201

        except MailGunException as errore:
            traceback.print_exc()
            return {
                "errore": prendi_testo("conferma_email_fallita"),
                "descrizione": errore,
            }, 500
        except:
            return {
                "errore": prendi_testo("conferma_inserimento"),
            }, 500
