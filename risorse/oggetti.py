from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from modelli.oggetti import ModelloOggetto


class Oggetto(Resource):
    """
    Classe API oggetto
    """
    # Questo è una proprietà statica che appartiene alla classe e non all'istanza
    # Permette di fare il parsing delle proprietà dell'oggetto
    parser = reqparse.RequestParser()
    parser.add_argument(
        'prezzo',
        type=float,
        required=True,
        help="Questo campo non può essere lasciato vuoto"
    )

    @jwt_required()
    def get(self, nome: str):
        oggetto = ModelloOggetto.trova_per_nome(nome)
        if oggetto:
            return oggetto.json()
        return {'errore': 'Oggetto non trovato'}, 404

    @jwt_required()
    def post(self, nome: str):
        if ModelloOggetto.trova_per_nome(nome):
            return {'errore': f"E' già presente un oggetto chiamato {nome}."}, 409

        dati = Oggetto.parser.parse_args()
        nuovo_oggetto = ModelloOggetto(nome, dati['prezzo'])

        try:
            nuovo_oggetto.inserisci()
        except:
            return {'errore': 'Si è verificato un errore inserendo l\'oggetto'}, 500

        return nuovo_oggetto.json(), 201

    @jwt_required()
    def delete(self, nome):
        if ModelloOggetto.trova_per_nome(nome):
            connessione = sqlite3.connect('./db/dati.db')
            cursore = connessione.cursor()

            query = "DELETE FROM oggetti WHERE nome=?;"
            cursore.execute(query, (nome,))
            connessione.commit()
            connessione.close()
            return {'messaggio': 'Oggetto eliminato'}
        else:
            return {'errore': f"Non è presente un oggetto chiamato {nome}."}, 404

    @jwt_required()
    def put(self, nome):
        dati = Oggetto.parser.parse_args()
        nuovo_oggetto = ModelloOggetto(nome, dati['prezzo'])
        oggetto_esistente = ModelloOggetto.trova_per_nome(nome)

        if oggetto_esistente:
            try:
                nuovo_oggetto.aggiorna()
            except:
                return {'errore': 'Si è verificato un errore aggiornando l\'oggetto'}, 500

            return nuovo_oggetto.json(), 200
        else:
            try:
                nuovo_oggetto.inserisci()
            except:
                return {'errore': 'Si è verificato un errore inserendo l\'oggetto'}, 500

            return nuovo_oggetto.json(), 201


class Oggetti(Resource):
    @jwt_required()
    def get(self):
        connessione = sqlite3.connect('./db/dati.db')
        cursore = connessione.cursor()

        query = "SELECT * FROM oggetti;"
        risultato = cursore.execute(query)

        oggetti = [{"nome": riga[0], "prezzo": riga [1]} for riga in risultato]

        connessione.close()

        return {'oggetti': oggetti}
