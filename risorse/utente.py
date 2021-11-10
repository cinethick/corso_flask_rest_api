"""
Classe utente dell'applicazione
"""
from flask import request
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
)
from flask_restful import Resource
from passlib.context import CryptContext

from modelli.utente import ModelloUtente
from schemi.utente import SchemaUtente

BLOCKLIST: set = set()
CONTESTO_PWD = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000,
)
MESSAGGI_UTENTE = {
    "campo": "Il campo '{}' non può essere lasciato vuoto.",
    "non_trovato": "Non è presente un utente con id {}.",
    "duplicato": "E' già presente un utente chiamato {}.",
    "inserito": "Utente inserito correttamente.",
    "inserimento": "Si è verificato un errore inserendo l'utente.",
    "modificazione": "Si è verificato un errore modificando l'utente.",
    "eliminato": "Utente eliminato.",
    "eliminazione": "Si è verificato un errore eliminando l'utente.",
    "non_autorizzato": "Azione non autorizzata!",
    "credenziali": "Credenziali non valide!",
    "logout": "Logout eseguito correttamente! (Utente ID {})",
    "attivato": "Utente attivato correttamente! (Utente ID {})",
    "non_attivato": "Non ha confermato la registrazione. Per piacere verifichi la sua email: {}.",
    "gia_attivato": "L'utente è già stato attivato. (Utente ID {})",
}

schema_utente = SchemaUtente()


class RegistraUtente(Resource):
    @classmethod
    def post(cls):
        json = request.get_json()
        utente = schema_utente.load(json)

        nuovo_hash = CONTESTO_PWD.hash(utente.password.encode("utf-8"))
        utente.password = nuovo_hash

        if ModelloUtente.trova_per_nome(utente.nome):
            return {"errore": MESSAGGI_UTENTE["duplicato"].format(utente.nome)}, 409

        utente.salva()

        return {"messaggio": MESSAGGI_UTENTE["inserito"]}, 201


class Utente(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def get(cls, id_utente: int):
        utente = ModelloUtente.trova_per_id(id_utente)
        if utente:
            return schema_utente.dump(utente)
        return {"errore": MESSAGGI_UTENTE["non_trovato"].format(id_utente)}, 404

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, id_utente: int):
        claims = get_jwt()
        if not claims["admin"]:
            return {"errore": MESSAGGI_UTENTE["non_autorizzato"]}, 401

        utente = ModelloUtente.trova_per_id(id_utente)
        if utente:
            try:
                utente.elimina()
            except:
                return {"errore": MESSAGGI_UTENTE["eliminazione"]}, 500

            return {"messaggio": MESSAGGI_UTENTE["eliminato"]}
        else:
            return {"errore": MESSAGGI_UTENTE["non_trovato"].format(id_utente)}, 404


class LoginUtente(Resource):
    @classmethod
    def post(cls):
        json = request.get_json()
        credenziali = schema_utente.load(json)

        utente = ModelloUtente.trova_per_nome(credenziali.nome)

        if utente and CONTESTO_PWD.verify(
            credenziali.password.encode("utf-8"), utente.password
        ):
            if utente.attivato:
                token_accesso = create_access_token(identity=utente.id, fresh=True)
                token_refresh = create_refresh_token(utente.id)
                return {
                    "access_token": token_accesso,
                    "refresh_token": token_refresh,
                }, 200

            return {"errore": MESSAGGI_UTENTE["non_attivato"].format(utente.nome)}, 401

        return {"errore": MESSAGGI_UTENTE["credenziali"]}, 401


class LogoutUtente(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        # jti = JWT ID
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        id_utente = get_jwt_identity()
        return {"messaggio": MESSAGGI_UTENTE["logout"].format(id_utente)}, 200


class ConfermaUtente(Resource):
    @classmethod
    def get(cls, id_utente: int):
        utente = ModelloUtente.trova_per_id(id_utente)
        if utente and not utente.attivato:
            try:
                utente.attivato = True
                utente.salva()
            except:
                return {"errore": MESSAGGI_UTENTE["modificazione"]}, 500

            return {"messaggio": MESSAGGI_UTENTE["attivato"].format(id_utente)}

        elif utente and utente.attivato:
            return {"errore": MESSAGGI_UTENTE["gia_attivato"].format(id_utente)}, 404

        else:
            return {"errore": MESSAGGI_UTENTE["non_trovato"].format(id_utente)}, 404
