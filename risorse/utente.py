"""
Classe utente dell'applicazione
"""
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt,
)
from flask_restful import Resource, reqparse
from passlib.context import CryptContext

from modelli.utente import ModelloUtente

BLOCKLIST: set = set()
CONTESTO_PWD = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000,
)


def parser_utente():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "nome",
        type=str,
        required=True,
        help="Questo campo non può essere lasciato vuoto",
    )
    parser.add_argument(
        "password",
        type=str,
        required=True,
        help="Questo campo non può essere lasciato vuoto",
    )
    return parser


class RegistraUtente(Resource):
    parser = parser_utente()

    @classmethod
    def post(cls):
        dati = cls.parser.parse_args()
        nome = dati["nome"]
        dati["password"] = CONTESTO_PWD.hash(dati["password"].encode("utf-8"))
        nuovo_utente = ModelloUtente(**dati)

        if ModelloUtente.trova_per_nome(nome):
            return {"errore": f"E' già presente un utente chiamato {nome}."}, 409

        nuovo_utente.salva()

        return {"messaggio": "Utente creato correttamente"}, 201


class Utente(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def get(cls, id_utente: int):
        utente = ModelloUtente.trova_per_id(id_utente)
        if utente:
            return utente.json()
        return {"errore": "Utente non trovato"}, 404

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, id_utente: int):
        claims = get_jwt()
        if not claims["admin"]:
            return {"errore": "Azione non autorizzata"}, 401

        utente = ModelloUtente.trova_per_id(id_utente)
        if utente:
            try:
                utente.elimina()
            except:
                return {"errore": "Si è verificato un errore eliminando l'utente."}, 500

            return {"messaggio": "Utente eliminato."}
        else:
            return {"errore": "Utente non trovato."}, 404


class LoginUtente(Resource):
    parser = parser_utente()

    @classmethod
    def post(cls):
        dati = cls.parser.parse_args()
        utente = ModelloUtente.trova_per_nome(dati["nome"])

        if utente and CONTESTO_PWD.verify(
            dati["password"].encode("utf-8"), utente.password
        ):
            token_accesso = create_access_token(identity=utente.id, fresh=True)
            token_refresh = create_refresh_token(utente.id)
            return {"access_token": token_accesso, "refresh_token": token_refresh}, 200
        return {"errore": "Credenziali non valide!"}, 401


class LogoutUtente(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        # jti = JWT ID
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"messaggio": "Logout eseguito correttamente."}, 200
