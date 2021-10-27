"""
Questo modulo contiene il necessario per verificare l'autenticità degli utenti
Sono stati temporaneamente create le liste utente
"""

from utente import Utente


def autenticazione(nome_utente: str, password: str):
    utente = Utente.trova_per_nome(nome_utente)
    if utente and utente.password == password:
        return utente


def identita(payload):
    id_utente = payload['identity']
    return Utente.trova_per_id(id_utente)
