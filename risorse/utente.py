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

    def post(self):
        dati = RegistraUtente.parser.parse_args()
        nome = dati['nome']
        nuovo_utente = ModelloUtente(**dati)

        if ModelloUtente.trova_per_nome(nome):
            return {'errore': f"E' già presente un utente chiamato {nome}."}, 409

        nuovo_utente.salva()

        return {'messaggio': 'Utente creato correttamente'}, 201
