from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from db.gestione import database
from risorse.negozio import Negozi, Negozio
from risorse.oggetto import Oggetto, Oggetti
from risorse.utente import RegistraUtente
from security import autenticazione, identita

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/dati.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ChiaveSegretaPerIlJWT!!!1!g'
api = Api(app)
database.init_app(app)


@app.before_first_request
def crea_tabelle():
    database.create_all()


jwt = JWT(app, autenticazione, identita)

api.add_resource(Oggetto, '/oggetto/<string:nome>')
api.add_resource(Oggetti, '/oggetti')
api.add_resource(Negozio, '/negozio/<string:nome>')
api.add_resource(Negozi, '/negozi')
api.add_resource(RegistraUtente, '/registra')

if __name__ == '__main__':
    app.run()
