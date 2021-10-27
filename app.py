from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import autenticazione, identita
from risorse.utente import RegistraUtente
from risorse.oggetti import Oggetto, Oggetti

app = Flask(__name__)
app.secret_key = 'ChiaveSegretaPerIlJWT!!!1!g'
api = Api(app)

jwt = JWT(app, autenticazione, identita)

api.add_resource(Oggetto, '/oggetto/<string:nome>')
api.add_resource(Oggetti, '/oggetti')
api.add_resource(RegistraUtente, '/registra')

if __name__ == '__main__':
    app.run()
