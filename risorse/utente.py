"""
Classe utente dell'applicazione
"""
from flask_restful import Resource, reqparse

from modelli.utente import ModelloUtente


class RegistraUtente(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'nome',
        type=str,
        required=True,
        help="Questo campo non può essere lasciato vuoto"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Questo campo non può essere lasciato vuoto"
    )

    @classmethod
    def post(cls):
        dati = cls.parser.parse_args()
        nome = dati['nome']
        nuovo_utente = ModelloUtente(**dati)

        if ModelloUtente.trova_per_nome(nome):
            return {'errore': f"E' già presente un utente chiamato {nome}."}, 409

        nuovo_utente.salva()

        return {'messaggio': 'Utente creato correttamente'}, 201


class Utente(Resource):
    @classmethod
    def get(cls, id_utente: int):
        utente = ModelloUtente.trova_per_id(id_utente)
        if utente:
            return utente.json()
        return {"errore": "Utente non trovato"}, 404

    @classmethod
    def delete(cls, id_utente: int):
        utente = ModelloUtente.trova_per_id(id_utente)
        if utente:
            try:
                utente.elimina()
            except:
                return {'errore': 'Si è verificato un errore eliminando l\'utente.'}, 500

            return {'messaggio': 'Utente eliminato.'}
        else:
            return {'errore': 'Utente non trovato.'}, 404

