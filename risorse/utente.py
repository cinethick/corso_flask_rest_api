"""
Classe utente dell'applicazione
"""
from flask import request
from marshmallow import ValidationError
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
    "eliminato": "Utente eliminato.",
    "eliminazione": "Si è verificato un errore eliminando l'utente.",
    "non_autorizzato": "Azione non autorizzata",
    "credenziali": "Credenziali non valide!",
    "logout": "Logout eseguito correttamente! (Utente ID {})",
    "validazione": "Errore di validazione dei dati.",
}

schema_utente = SchemaUtente()


class RegistraUtente(Resource):
    @classmethod
    def post(cls):
        try:
            json = request.get_json()
            dati = schema_utente.load(json)
        except ValidationError as errore:
            return {
                "errore": MESSAGGI_UTENTE["validazione"],
                "descrizione": errore,
            }, 400

        nome = dati["nome"]
        dati["password"] = CONTESTO_PWD.hash(dati["password"].encode("utf-8"))
        nuovo_utente = ModelloUtente(**dati)

        if ModelloUtente.trova_per_nome(nome):
            return {"errore": MESSAGGI_UTENTE["duplicato"].format(nome)}, 409

        nuovo_utente.salva()

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
        try:
            json = request.get_json()
            dati = schema_utente.load(json)
        except ValidationError as errore:
            return {
                "errore": MESSAGGI_UTENTE["validazione"],
                "descrizione": errore,
            }, 400

        utente = ModelloUtente.trova_per_nome(dati["nome"])

        if utente and CONTESTO_PWD.verify(
            dati["password"].encode("utf-8"), utente.password
        ):
            token_accesso = create_access_token(identity=utente.id, fresh=True)
            token_refresh = create_refresh_token(utente.id)
            return {"access_token": token_accesso, "refresh_token": token_refresh}, 200
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
