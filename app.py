from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import autenticazione, identita

app = Flask(__name__)
app.secret_key = 'ChiaveSegretaPerIlJWT!!!1!g'
api = Api(app)

jwt = JWT(app, autenticazione, identita)
# crea un nuovo endpoint che si chiama /auth
# quando si chiama /auth si manda l'username e la password
# jwt usa "autenticazione" per verificare l'utente
# jwt ritorna il JWT token che poi viene immagazzinato dal client

oggetti = []


class Oggetto(Resource):
    """
    Classe API oggetto
    """
    @jwt_required()
    def get(self, nome: str):
        oggetto_cercato = next(filter(lambda oggetto: oggetto['name'] == nome, oggetti), None)
        # Si crea un oggetto filtro e si usa next( ..., None) per ritornare None se la lista è vuota
        return {'oggetti': oggetto_cercato}, 200 if oggetto_cercato else 404

    @jwt_required()
    def post(self, nome: str):
        # verifica che non esista un oggetto con lo stesso nome
        if next(filter(lambda oggetto: oggetto['name'] == nome, oggetti), None):
            return {'errore': f"E' già presente un oggetto chiamato {nome}."}, 409

        dati = request.get_json()
        oggetto = {'nome': nome, 'prezzo': dati.get('prezzo', 0)}
        oggetti.append(oggetto)
        return oggetto, 201


class Oggetti(Resource):
    @jwt_required()
    def get(self):
        return {'oggetti': oggetti}


api.add_resource(Oggetto, '/oggetto/<string:nome>')
api.add_resource(Oggetti, '/oggetti')

if __name__ == '__main__':
    app.run()
