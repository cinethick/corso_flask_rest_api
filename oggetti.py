from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


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

    @classmethod
    def trova_per_nome(cls, nome):
        connessione = sqlite3.connect('./db/dati.db')
        cursore = connessione.cursor()

        query = "SELECT * FROM oggetti WHERE nome=?;"
        risultato = cursore.execute(query, (nome,))
        riga = risultato.fetchone()
        connessione.close()
        if riga:
            return {'nome': riga[0], 'prezzo': riga[1]}

    @classmethod
    def inserisci(cls, nome: str, prezzo: float):
        connessione = sqlite3.connect('./db/dati.db')
        cursore = connessione.cursor()

        query = "INSERT INTO oggetti VALUES (?, ?);"
        cursore.execute(query, (nome, prezzo))
        cursore.commit()
        connessione.close()

    @classmethod
    def aggiorna(cls, nome: str, prezzo: float):
        connessione = sqlite3.connect('./db/dati.db')
        cursore = connessione.cursor()

        query = "UPDATE oggetti SET prezzo=? WHERE nome = ?;"
        cursore.execute(query, (nome, prezzo))
        cursore.commit()
        connessione.close()

    @jwt_required()
    def get(self, nome: str):
        oggetto = self.trova_per_nome(nome)
        if oggetto:
            return oggetto
        return {'errore': 'Oggetto non trovato'}, 404

    @jwt_required()
    def post(self, nome: str):
        if self.trova_per_nome(nome):
            return {'errore': f"E' già presente un oggetto chiamato {nome}."}, 409

        dati = Oggetto.parser.parse_args()
        nuovo_oggetto = {'nome': nome, 'prezzo': dati['prezzo']}

        try:
            self.inserisci(**nuovo_oggetto)
        except:
            return {'errore': 'Si è verificato un errore inserendo l\'oggetto'}, 500

        return nuovo_oggetto, 201

    @jwt_required()
    def delete(self, nome):
        if self.trova_per_nome(nome):
            connessione = sqlite3.connect('./db/dati.db')
            cursore = connessione.cursor()

            query = "DELETE FROM oggetti WHERE nome=?;"
            cursore.execute(query, (nome,))
            cursore.commit()
            connessione.close()
            return {'messaggio': 'Oggetto eliminato'}
        else:
            return {'errore': f"Non è presente un oggetto chiamato {nome}."}, 404

    @jwt_required()
    def put(self, nome):
        dati = Oggetto.parser.parse_args()
        nuovo_oggetto = {'nome': nome, 'prezzo': dati['prezzo']}
        oggetto_esistente = self.trova_per_nome(nome)

        if oggetto_esistente:
            try:
                self.aggiorna(**nuovo_oggetto)
            except:
                return {'errore': 'Si è verificato un errore aggiornando l\'oggetto'}, 500

            return oggetto_esistente, 200
        else:
            try:
                self.inserisci(**nuovo_oggetto)
            except:
                return {'errore': 'Si è verificato un errore inserendo l\'oggetto'}, 500

            return nuovo_oggetto, 201


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
