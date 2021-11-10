from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from marshmallow import ValidationError

from db.gestione import database
from schemi.validazione import validazione
from risorse.negozio import Negozi, Negozio
from risorse.oggetto import Oggetto, Oggetti
from risorse.utente import (
    RegistraUtente,
    Utente,
    LoginUtente,
    LogoutUtente,
    BLOCKLIST,
    ConfermaUtente,
)
from risorse.token_refresh import TokenRefresh

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/dati.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLOCKLIST_ENABLED"] = True
app.config["JWT_BLOCKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.config["JWT_SECRET_KEY"] = "ChiaveSegretaPerilJWT!!!1!g"
app.secret_key = "ChiaveSegretaPerlApplicazione!!!1!g"
api = Api(app)
database.init_app(app)
validazione.init_app(app)


@app.before_first_request
def crea_tabelle():
    database.create_all()


@app.errorhandler(ValidationError)
def gestisci_validazione_marshmallow(errore):
    return {
        "errore": "Errore di validazione dei dati.",
        "descrizione": errore.messages,
    }, 400


jwt = JWTManager(app)


@jwt.additional_claims_loader
def aggiunge_claims_al_jwt(identita: int):
    # qui vanno aggiunti tutte le configurazioni extra che vanno nel JWT, tipo admin ecc
    return {"admin": identita == 1}


@jwt.expired_token_loader
def callback_token_scaduti(jwt_header, jwt_payload):
    return (
        jsonify(
            {"errore": "token_scaduto", "errore_descrizione": "Il token è scaduto."}
        ),
        401,
    )


@jwt.invalid_token_loader
def callback_token_invalido(errore):
    return (
        jsonify(
            {
                "errore": "token_invalido",
                "errore_descrizione": "Verifica della firma fallita.",
            }
        ),
        401,
    )


@jwt.unauthorized_loader
def callback_token_mancante(errore):
    return (
        jsonify(
            {
                "errore": "autorizzazione_richiesta",
                "errore_descrizione": "La richiesta non contiene un token di accesso.",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def callback_token_non_fresco(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "errore": "richiesto_token_fresco",
                "errore_descrizione": "Il token non è fresco.",
            }
        ),
        401,
    )


@jwt.revoked_token_loader
def callback_token_revocato(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "errore": "token_revocato",
                "errore_descrizione": "Il token è stato revocato.",
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
api.add_resource(LoginUtente, "/login")
api.add_resource(LogoutUtente, "/logout")
api.add_resource(ConfermaUtente, "/conferma/<int:id_utente>")
api.add_resource(TokenRefresh, "/refresh")

if __name__ == "__main__":
    app.run()
