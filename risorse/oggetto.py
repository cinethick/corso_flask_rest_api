from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from libs.testi import prendi_testo
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
        return {"errore": prendi_testo("oggetto_non_trovato")}, 404

    @classmethod
    @jwt_required()
    def post(cls, nome: str):
        if ModelloOggetto.trova_per_nome(nome):
            return {"errore": prendi_testo("oggetto_duplicato").format(nome)}, 409

        json = request.get_json()
        json["nome"] = nome
        oggetto = schema_oggetto.load(json)

        try:
            oggetto.salva()
            return schema_oggetto.dump(oggetto), 201
        except:
            return {"errore": prendi_testo("oggetto_inserimento")}, 500

    @classmethod
    @jwt_required()
    def delete(cls, nome: str):
        oggetto_esistente = ModelloOggetto.trova_per_nome(nome)
        if oggetto_esistente:
            try:
                oggetto_esistente.elimina()
            except:
                return {"errore": prendi_testo("oggetto_eliminazione")}, 500

            return {"messaggio": prendi_testo("oggetto_eliminato")}
        else:
            return {"errore": prendi_testo("oggetto_non_trovato").format(nome)}, 404

    @classmethod
    @jwt_required()
    def put(cls, nome: str):
        json = request.get_json()
        json["nome"] = nome
        nuovo_oggetto = schema_oggetto.load(json)

        oggetto = ModelloOggetto.trova_per_nome(nome)

        if oggetto:
            oggetto.prezzo = nuovo_oggetto.prezzo
            oggetto.negozio_id = nuovo_oggetto.negozio_id
            codice = 200
        else:
            oggetto = nuovo_oggetto
            codice = 201

        try:
            oggetto.salva()
        except:
            return {"errore": prendi_testo("oggetto_inserimento")}, 500

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
            "messaggio": prendi_testo("credenziali"),
        }, 200
