"""
Questo modulo contiene il necessario per verificare l'autenticità degli utenti
Sono stati temporaneamente create le liste utente
"""

from hmac import compare_digest
from modelli.utente import ModelloUtente


def autenticazione(nome: str, password: str):
    utente = ModelloUtente.trova_per_nome(nome)
    if utente and compare_digest(utente.password.encode('utf-8'), password.encode('utf-8')):
        return utente


def identita(payload):
    id_utente = payload['identity']
    utente = ModelloUtente.trova_per_id(id_utente)
    return utente
