import sqlite3

# Connette al DB esistente o ne crea uno nuovo, aprendo il cursore
connessione = sqlite3.connect('dati.db')
cursore = connessione.cursor()

# Creare tabella (pattern 1, query statica)
crea_tabella_utenti = "CREATE TABLE utenti (id int, nome text, password text)"
cursore.execute(crea_tabella_utenti)

# Creare tabella (pattern 2, query con parametri (tupla!))
inserisci_utente = "INSERT INTO utenti VALUES (?, ?, ?)"
utente = (1, 'Matteo', 'semplice')
cursore.execute(inserisci_utente, utente)

# Creare tabella (pattern 3, query multipla
utenti = [
    (2, 'Prova1', 'semplicissima'),
    (3, 'Prova2', 'ancorapiusemplice')
]
cursore.executemany(inserisci_utente,utenti)

# Committare le modifiche e chiudere la connessione!
connessione.commit()
connessione.close()
