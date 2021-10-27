"""
Modello dell'Oggetto
"""

import sqlite3


class ModelloOggetto:
    def __init__(self, nome: str, prezzo: float):
        self.nome = nome
        self.prezzo = prezzo

    def json(self) -> dict:
        return {"nome": self.nome, "prezzo": self.prezzo}

    @classmethod
    def trova_per_nome(cls, nome) -> "ModelloOggetto":
        connessione = sqlite3.connect('./db/dati.db')
        cursore = connessione.cursor()

        query = "SELECT * FROM oggetti WHERE nome=?;"
        risultato = cursore.execute(query, (nome,))
        riga = risultato.fetchone()
        connessione.close()
        if riga:
            return cls(*riga)

    def inserisci(self):
        connessione = sqlite3.connect('./db/dati.db')
        cursore = connessione.cursor()

        query = "INSERT INTO oggetti VALUES (?, ?);"
        cursore.execute(query, (self.nome, self.prezzo))
        connessione.commit()
        connessione.close()

    def aggiorna(self):
        connessione = sqlite3.connect('./db/dati.db')
        cursore = connessione.cursor()

        query = "UPDATE oggetti SET prezzo=? WHERE nome = ?;"
        cursore.execute(query, (self.nome, self.prezzo))
        connessione.commit()
        connessione.close()
