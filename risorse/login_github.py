from flask import g, request, url_for
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource

from libs.oauth import github
from modelli.utente import ModelloUtente


class LoginGitHub(Resource):
    @classmethod
    def get(cls):
        return github.authorize(
            callback=url_for("autorizzazione.github", _external=True)
        )


class AutorizzazioneGitHub(Resource):
    @classmethod
    def get(cls):
        risposta = github.authorized_response()

        if risposta is None or risposta.get("access_token") is None:
            return {
                "errore": request.args["error"],
                "errore_descrizione": request.args["error_description"],
            }, 500

        g.access_token = risposta["access_token"]
        utente_github = github.get("user")
        nome_utente_github = utente_github.data["login"]

        utente = ModelloUtente.trova_per_nome(nome_utente_github)

        if not utente:
            utente = ModelloUtente(nome=nome_utente_github, password=None)
            utente.salva()

        token_accesso = create_access_token(identity=utente.id, fresh=True)
        token_refresh = create_refresh_token(utente.id)

        return {
            "access_token": token_accesso,
            "refresh_token": token_refresh,
        }, 200
