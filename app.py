from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

# Flask-Uploads da un errore di import. E' necessario installarlo direttamente da GitHub o fixarlo
from flask_uploads import configure_uploads, patch_request_class
from marshmallow import ValidationError

from db.gestione import database
from flask_migrate import Migrate
from libs.oauth import oauth
from libs.gestione_immagini import SET_IMMAGINI
from libs.testi import prendi_testo
from risorse.conferma import Conferma, ConfermaUtente
from risorse.immagine import UploadImmagine, Immagine, AvatarUpload, Avatar
from risorse.negozio import Negozi, Negozio
from risorse.oggetto import Oggetto, Oggetti
from risorse.ordine import Ordine
from risorse.token_refresh import TokenRefresh
from risorse.utente import (
    RegistraUtente,
    Utente,
    LoginUtente,
    LogoutUtente,
    BLOCKLIST,
    ReimpostaPassword,
)
from risorse.login_github import LoginGitHub, AutorizzazioneGitHub
from schemi.validazione import validazione

app = Flask(__name__)
load_dotenv(".env", verbose=True)
# Carica la configurazione dal file default_config.py
app.config.from_object("default_config")
# Carica la configurazione dal file indicato nel file .env alla variabile APPLICATION_SETTINGS
app.config.from_envvar("APPLICATION_SETTINGS")
patch_request_class(app, 10 * 1024 * 1024)  # limite di upload globale di 10MB
configure_uploads(app, SET_IMMAGINI)

api = Api(app)
database.init_app(app)
validazione.init_app(app)
# Aggiunto render_as_batch per gestire le migrazioni con SQLite, eliminare per PostgreSQL
migrazione = Migrate(app, database, render_as_batch=True)
oauth.init_app(app)


@app.before_first_request
def crea_tabelle():
    database.create_all()


@app.errorhandler(ValidationError)
def gestisci_validazione_marshmallow(errore):
    return {
        "errore": prendi_testo("app_errore_validazione"),
        "validazione": errore.messages,
    }, 400


jwt = JWTManager(app)


@jwt.additional_claims_loader
def aggiunge_claims_al_jwt(identita: int):
    # qui vanno aggiunti tutte le configurazioni extra che vanno nel JWT, tipo admin ecc
    return {"admin": identita == 1}


@jwt.expired_token_loader
def callback_token_scaduti(jwt_header, jwt_payload):
    return (
        jsonify({"errore": prendi_testo("app_errore_token_scaduto")}),
        401,
    )


@jwt.invalid_token_loader
def callback_token_invalido(errore):
    return (
        jsonify(
            {
                "errore": prendi_testo("app_errore_token_invalido"),
            }
        ),
        401,
    )


@jwt.unauthorized_loader
def callback_token_mancante(errore):
    return (
        jsonify(
            {
                "errore": prendi_testo("app_errore_token_mancante"),
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def callback_token_non_fresco(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "errore": prendi_testo("app_errore_token_non_fresco"),
            }
        ),
        401,
    )


@jwt.revoked_token_loader
def callback_token_revocato(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "errore": prendi_testo("app_errore_token_revocato"),
            }
        ),
        401,
    )


@jwt.token_in_blocklist_loader
def verifica_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


api.add_resource(Oggetto, "/oggetto/<string:nome>")
api.add_resource(Oggetti, "/oggetti")
api.add_resource(Negozio, "/negozio/<string:nome>")
api.add_resource(Negozi, "/negozi")
api.add_resource(RegistraUtente, "/registra")
api.add_resource(Utente, "/utente/<int:id_utente>")
api.add_resource(ReimpostaPassword, "/utente/password")
api.add_resource(LoginUtente, "/login")
api.add_resource(LogoutUtente, "/logout")
api.add_resource(Conferma, "/conferma/<string:id_conferma>")
api.add_resource(ConfermaUtente, "/conferma/utente/<int:id_utente>")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UploadImmagine, "/upload/immagini")
api.add_resource(Immagine, "/immagine/<string:nome_immagine>")
api.add_resource(AvatarUpload, "/upload/avatar")
api.add_resource(Avatar, "/avatar/<int:id_utente>")
api.add_resource(LoginGitHub, "/login/github")
api.add_resource(
    AutorizzazioneGitHub, "/login/github/authorized", endpoint="autorizzazione.github"
)
api.add_resource(Ordine, "/ordine")

if __name__ == "__main__":
    app.run()
