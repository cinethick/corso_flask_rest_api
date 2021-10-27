"""
Classe utente dell'applicazione
"""
import sqlite3
from flask_restful import Resource, reqparse


class Utente:
    """Classe che rappresenta un utente dell'applicazione"""
    def __init__(self, _id: int, nome_utente: str, password: str):
        self.id = _id
        self.nome = nome_utente
        self.password = password

    @classmethod
    def trova_per_nome(cls, nome_utente: str):
        connessione = sqlite3.connect('./db/dati.db')
        cursore = connessione.cursor()
        query = "SELECT * FROM utenti WHERE nome=?;"
        risultato = cursore.execute(query, (nome_utente,))
        riga = risultato.fetchone()
        if riga:
            utente = cls(*riga)
        else:
            utente = None
        connessione.close()
        return utente

    @classmethod
    def trova_per_id(cls, _id: int):
        connessione = sqlite3.connect('./db/dati.db')
        cursore = connessione.cursor()
        query = "SELECT * FROM utenti WHERE id=?;"
        risultato = cursore.execute(query, (_id,))
        riga = risultato.fetchone()
        if riga:
            utente = cls(*riga)
        else:
            utente = None
        connessione.close()
        return utente


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

        if Utente.trova_per_nome(nome):
            return {'errore': f"E' già presente un utente chiamato {nome}."}, 409

        connessione = sqlite3.connect('./db/dati.db')
        cursore = connessione.cursor()

        query = "INSERT INTO utenti VALUES (NULL, ?, ?)"
        cursore.execute(query, (nome, dati['password']))
        cursore.commit()
        cursore.close()

        return {'messaggio': 'Utente creato correttamente'}, 201
