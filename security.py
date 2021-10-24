"""
Questo modulo contiene il necessario per verificare l'autenticità degli utenti
Sono stati temporaneamente create le liste utente
"""

from utente import Utente

utenti = [
    Utente(1, 'Matteo', 'Password!')
]

mappa_nomi_utente = {utn.nome: utn for utn in utenti}

mappa_id_utente = {utn.id: utn for utn in utenti}


def autenticazione(nome_utente: str, password: str):
    utente = mappa_nomi_utente.get(nome_utente, None)
    if utente and utente.password == password:
        return utente


def identita(payload):
    id_utente = payload['identity']
    return mappa_id_utente.get(id_utente, None)
