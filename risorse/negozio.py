from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from modelli.negozio import ModelloNegozio
from schemi.negozio import SchemaNegozio

MESSAGGI_NEGOZIO = {
    "campo": "Il campo '{}' non può essere lasciato vuoto.",
    "non_trovato": "Non è presente un negozio chiamato {}.",
    "duplicato": "E' già presente un negozio chiamato {}.",
    "inserimento": "Si è verificato un errore inserendo il negozio.",
    "eliminato": "Negozio eliminato.",
    "eliminazione": "Si è verificato un errore eliminando il negozio.",
    "credenziali": "I dati completi richiedono l'autenticazione.",
}

schema_negozio = SchemaNegozio()


class Negozio(Resource):
    """
    Classe API negozio
    """

    @jwt_required()
    def get(self, nome: str):
        negozio = ModelloNegozio.trova_per_nome(nome)
        if negozio:
            return schema_negozio.dump(negozio)
        return {"errore": MESSAGGI_NEGOZIO["non_trovato"].format(nome)}, 404

    @classmethod
    @jwt_required()
    def post(cls, nome: str):
        if ModelloNegozio.trova_per_nome(nome):
            return {"errore": MESSAGGI_NEGOZIO["duplicato"].format(nome)}, 409

        nuovo_negozio = ModelloNegozio(nome)  # (nome=nome)?

        try:
            nuovo_negozio.salva()
        except:
            return {"errore": MESSAGGI_NEGOZIO["inserimento"]}, 500

        return schema_negozio.dump(nuovo_negozio), 201

    @classmethod
    @jwt_required()
    def delete(cls, nome):
        negozio_esistente = ModelloNegozio.trova_per_nome(nome)
        if negozio_esistente:
            try:
                negozio_esistente.elimina()
            except:
                return {"errore": MESSAGGI_NEGOZIO["eliminazione"]}, 500

            return {"messaggio": MESSAGGI_NEGOZIO["eliminato"]}
        else:
            return {"errore": MESSAGGI_NEGOZIO["non_trovato"].format(nome)}, 404


class Negozi(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls):
        id_utente = get_jwt_identity()
        negozi = [
            schema_negozio.dump(negozio) for negozio in ModelloNegozio.trova_tutti()
        ]
        if id_utente:
            return {"negozi": negozi}
        return {
            "oggetti": [negozio["nome"] for negozio in negozi],
            "messaggio": MESSAGGI_NEGOZIO["credenziali"],
        }, 200
