from flask import request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from modelli.oggetto import ModelloOggetto
from schemi.oggetto import SchemaOggetto

MESSAGGI_OGGETTO = {
    "campo": "Il campo '{}' non può essere lasciato vuoto.",
    "non_trovato": "Non è presente un oggetto chiamato {}.",
    "duplicato": "E' già presente un oggetto chiamato {}.",
    "inserimento": "Si è verificato un errore inserendo l'oggetto.",
    "eliminato": "Oggetto eliminato.",
    "eliminazione": "Si è verificato un errore eliminando l'oggetto.",
    "credenziali": "I dati completi richiedono l'autenticazione",
    "validazione": "Errore di validazione dei dati.",
}

schema_oggetto = SchemaOggetto()


class Oggetto(Resource):
    """
    Classe API oggetto
    """

    # Questo è una proprietà statica che appartiene alla classe e non all'istanza
    # Permette di fare il parsing delle proprietà dell'oggetto

    @classmethod
    @jwt_required()
    def get(cls, nome: str):
        oggetto = ModelloOggetto.trova_per_nome(nome)
        if oggetto:
            return schema_oggetto.dump(oggetto)
        return {"errore": MESSAGGI_OGGETTO["non_trovato"]}, 404

    @classmethod
    @jwt_required()
    def post(cls, nome: str):
        if ModelloOggetto.trova_per_nome(nome):
            return {"errore": MESSAGGI_OGGETTO["duplicato"].format(nome)}, 409

        try:
            json = request.get_json()
            dati = schema_oggetto.load(json)
        except ValidationError as errore:
            return {
                "errore": MESSAGGI_OGGETTO["validazione"],
                "descrizione": errore.messages,
            }, 400

        try:
            nuovo_oggetto = ModelloOggetto(nome, dati["prezzo"], dati["negozio_id"])
            nuovo_oggetto.salva()
            return schema_oggetto.dump(nuovo_oggetto), 201
        except:
            return {"errore": MESSAGGI_OGGETTO["inserimento"]}, 500

    @classmethod
    @jwt_required()
    def delete(cls, nome):
        oggetto_esistente = ModelloOggetto.trova_per_nome(nome)
        if oggetto_esistente:
            try:
                oggetto_esistente.elimina()
            except:
                return {"errore": MESSAGGI_OGGETTO["eliminazione"]}, 500

            return {"messaggio": MESSAGGI_OGGETTO["eliminato"]}
        else:
            return {"errore": MESSAGGI_OGGETTO["non_trovato"].format(nome)}, 404

    @classmethod
    @jwt_required()
    def put(cls, nome):
        try:
            json = request.get_json()
            dati = schema_oggetto.load(json)
        except ValidationError as errore:
            return {
                "errore": MESSAGGI_OGGETTO["validazione"],
                "descrizione": errore.messages,
            }, 400

        oggetto = ModelloOggetto.trova_per_nome(nome)

        if oggetto:
            oggetto.prezzo = dati["prezzo"]
            oggetto.negozio_id = dati["negozio_id"]
            codice = 200
        else:
            oggetto = ModelloOggetto(nome, **dati)
            codice = 201

        try:
            oggetto.salva()
        except:
            return {"errore": MESSAGGI_OGGETTO["inserimento"]}, 500

        return schema_oggetto.dump(oggetto), codice


class Oggetti(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls):
        id_utente = get_jwt_identity()
        oggetti = [
            schema_oggetto.dump(oggetto) for oggetto in ModelloOggetto.trova_tutti()
        ]
        if id_utente:
            return {"oggetti": oggetti}
        return {
            "oggetti": [oggetto["nome"] for oggetto in oggetti],
            "messaggio": MESSAGGI_OGGETTO["credenziali"],
        }, 200
