import traceback
from time import time

from flask import make_response, render_template
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource

from libs.mailgun import MailGunException
from modelli.conferma import ModelloConferma
from modelli.utente import ModelloUtente
from schemi.conferma import SchemaConferma

MESSAGGI_CONFERMA = {
    "campo": "Il campo '{}' non può essere lasciato vuoto.",
    "non_trovato": "Il codice di conferma non è valido.",
    "utente_non_trovato": "Non è stata trovato un codice di conferma valido per questo utente",
    "scaduta": "La conferma è scaduta. Si prega di richiedere un nuovo codice di conferma.",
    "inserito": "E' stata inviata una nuova email per confermare l'attivazione dell'account.",
    "inserimento": "Si è verificato un errore creando la nuova azione di conferma dell'account.",
    "modificazione": "Si è verificato un errore modificando la conferma.",
    "eliminato": "Conferma eliminata.",
    "eliminazione": "Si è verificato un errore eliminando la conferma.",
    "email_fallita": "Si è verificato un errore inviando l'email di attivazione!",
    "non_autorizzato": "Azione non autorizzata!",
    "credenziali": "Credenziali non valide!",
    "attivato": "Utente attivato correttamente! (Utente ID {})",
    "non_attivato": "Non ha confermato la registrazione. Per piacere verifichi la sua email: {}.",
    "gia_attivato": "L'account risulta già attivato.",
}

schema_conferma = SchemaConferma()


class Conferma(Resource):
    @classmethod
    def get(cls, id_conferma: str):
        conferma = ModelloConferma.trova_per_id(id_conferma)

        if not conferma:
            return {"errore": MESSAGGI_CONFERMA["non_trovato"]}, 404

        if conferma.confermata:
            return {"errore": MESSAGGI_CONFERMA["gia_attivato"]}, 400

        if conferma.e_scaduta:
            return {"errore": MESSAGGI_CONFERMA["scaduta"]}, 400

        try:
            conferma.confermata = True
            conferma.porta_a_scadenza()  # salva
        except:
            return {"errore": MESSAGGI_CONFERMA["modificazione"]}, 500

        return make_response(
            render_template("conferma.html", email=conferma.utente.email),
            200,
            {"Content-Type": "text/html"},
        )


class ConfermaUtente(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def get(cls, id_utente: int):
        claims = get_jwt()
        if not claims["admin"]:
            return {
                "errore": MESSAGGI_CONFERMA["non_autorizzato"],
                "suggerimento": "Per creare una nuova email di conferma inviare la richiesta con il verbo POST.",
            }, 401

        utente = ModelloUtente.trova_per_id(id_utente)

        if not utente:
            return {"errore": MESSAGGI_CONFERMA["utente_non_trovato"]}, 404

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
            return {"errore": MESSAGGI_CONFERMA["utente_non_trovato"]}, 404

        try:
            conferma = utente.conferma_piu_recente

            if conferma:
                if conferma.confermata:
                    return {"errore": MESSAGGI_CONFERMA["gia_attivato"]}, 400
                conferma.porta_a_scadenza()

            nuova_conferma = ModelloConferma(id_utente)
            nuova_conferma.salva()
            utente.invia_conferma_email()
            return {"messaggio": MESSAGGI_CONFERMA["inserito"]}, 201

        except MailGunException as errore:
            traceback.print_exc()
            return {
                "errore": MESSAGGI_CONFERMA["email_fallita"],
                "descrizione": errore,
            }, 500
        except:
            return {
                "errore": MESSAGGI_CONFERMA["inserimento"],
            }, 500
