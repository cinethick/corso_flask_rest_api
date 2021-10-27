import sqlite3


class ModelloUtente:
    """Classe che rappresenta un utente dell'applicazione"""
    def __init__(self, _id: int, nome: str, password: str):
        self.id = _id
        self.nome = nome
        self.password = password

    def json(self):
        return {"nome": self.nome, "password": self.password}

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

    def inserisci(self):
        connessione = sqlite3.connect('./db/dati.db')
        cursore = connessione.cursor()

        query = "INSERT INTO utenti VALUES (NULL, ?, ?)"
        cursore.execute(query, (self.nome, self.password))
        connessione.commit()
        cursore.close()
