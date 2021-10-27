import sqlite3


class ModelloUtente:
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