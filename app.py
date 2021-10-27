from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import autenticazione, identita
from utente import RegistraUtente
from oggetti import Oggetto, Oggetti

app = Flask(__name__)
app.secret_key = 'ChiaveSegretaPerIlJWT!!!1!g'
api = Api(app)

jwt = JWT(app, autenticazione, identita)
# crea un nuovo endpoint che si chiama /auth
# quando si chiama /auth si manda l'username e la password
# jwt usa "autenticazione" per verificare l'utente
# jwt ritorna il JWT token che poi viene immagazzinato dal client

api.add_resource(Oggetto, '/oggetto/<string:nome>')
api.add_resource(Oggetti, '/oggetti')
api.add_resource(RegistraUtente, '/registra')

if __name__ == '__main__':
    app.run()
