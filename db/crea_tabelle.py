"""
Questo modulo crea le tabelle nel database
"""
import sqlite3

connessione = sqlite3.connect('./dati.db')
cursore = connessione.cursor()

crea_tabella_utenti = "CREATE TABLE IF NOT EXISTS utenti (id INTEGER PRIMARY KEY, nome TEXT, password TEXT);"
cursore.execute(crea_tabella_utenti)

crea_tabella_oggetti = "CREATE TABLE IF NOT EXISTS oggetti (nome TEXT, prezzo REAL);"
cursore.execute(crea_tabella_oggetti)

connessione.commit()
connessione.close()
