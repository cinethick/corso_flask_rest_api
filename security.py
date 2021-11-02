"""
Questo modulo contiene il necessario per verificare l'autenticità degli utenti
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


# @jwt.auth_response_handler
# def gestore_risposta(token_accesso, utente):
#     return jsonify({
#         "token_accesso": token_accesso.decode('utf-8'),
#         "id_utente": utente.id
#     })


# @jwt.error_handler
# def gestore_errori(errore):
#     return jsonify({
#         "messaggio": errore.description,
#         "codice": errore.status_code
#     }), errore.status_code
