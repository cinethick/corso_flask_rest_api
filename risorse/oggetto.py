from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from modelli.oggetto import ModelloOggetto


MESSAGGI_OGGETTO = {
    "campo": "Il campo '{}' non può essere lasciato vuoto.",
    "non_trovato": "Non è presente un oggetto chiamato {}.",
    "duplicato": "E' già presente un oggetto chiamato {}.",
    "inserimento": "Si è verificato un errore inserendo l'oggetto.",
    "eliminato": "Oggetto eliminato.",
    "eliminazione": "Si è verificato un errore eliminando l'oggetto.",
    "credenziali": "I dati completi richiedono l'autenticazione",
}


class Oggetto(Resource):
    """
    Classe API oggetto
    """

    # Questo è una proprietà statica che appartiene alla classe e non all'istanza
    # Permette di fare il parsing delle proprietà dell'oggetto
    parser = reqparse.RequestParser()
    parser.add_argument(
        "prezzo",
        type=float,
        required=True,
        help=MESSAGGI_OGGETTO["campo"].format("prezzo"),
    )
    parser.add_argument(
        "negozio_id",
        type=int,
        required=True,
        help=MESSAGGI_OGGETTO["campo"].format("negozio_id"),
    )

    @jwt_required()
    def get(self, nome: str):
        oggetto = ModelloOggetto.trova_per_nome(nome)
        if oggetto:
            return oggetto.json()
        return {"errore": MESSAGGI_OGGETTO["non_trovato"]}, 404

    @jwt_required()
    def post(self, nome: str):
        if ModelloOggetto.trova_per_nome(nome):
            return {"errore": MESSAGGI_OGGETTO["duplicato"].format(nome)}, 409

        dati = Oggetto.parser.parse_args()
        nuovo_oggetto = ModelloOggetto(nome, dati["prezzo"], dati["negozio_id"])

        try:
            nuovo_oggetto.salva()
        except:
            return {"errore": MESSAGGI_OGGETTO["inserimento"]}, 500

        return nuovo_oggetto.json(), 201

    @jwt_required()
    def delete(self, nome):
        oggetto_esistente = ModelloOggetto.trova_per_nome(nome)
        if oggetto_esistente:
            try:
                oggetto_esistente.elimina()
            except:
                return {"errore": MESSAGGI_OGGETTO["eliminazione"]}, 500

            return {"messaggio": MESSAGGI_OGGETTO["eliminato"]}
        else:
            return {"errore": MESSAGGI_OGGETTO["non_trovato"].format(nome)}, 404

    @jwt_required()
    def put(self, nome):
        dati = Oggetto.parser.parse_args()
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

        return oggetto.json(), codice


class Oggetti(Resource):
    @jwt_required(optional=True)
    def get(self):
        id_utente = get_jwt_identity()
        oggetti = [oggetto.json() for oggetto in ModelloOggetto.trova_tutti()]
        if id_utente:
            return {"oggetti": oggetti}
        return {
            "oggetti": [oggetto["nome"] for oggetto in oggetti],
            "messaggio": MESSAGGI_OGGETTO["credenziali"],
        }, 200
