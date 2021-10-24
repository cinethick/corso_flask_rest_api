from flask import Flask
from flask_restful import Resource, Api, reqparse
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
    # Questo è una proprietà statica che appartiene alla classe e non all'istanza
    # Permette di fare il parsing delle proprietà dell'oggetto
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="Questo campo non può essere lasciato vuoto"
    )

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

        dati = Oggetto.parser.parse_args()
        nuovo_oggetto = {'nome': nome, 'prezzo': dati.get('prezzo', 0)}
        oggetti.append(nuovo_oggetto)
        return nuovo_oggetto, 201

    @jwt_required()
    def delete(self, nome):
        global oggetti
        if next(filter(lambda oggetto: oggetto['name'] == nome, oggetti), None):
            oggetti = list(filter(lambda oggetto: oggetto['nome'] != nome, oggetti))
            return {'messaggio': 'Oggetto eliminato'}
        else:
            return {'errore': f"Non è presente un oggetto chiamato {nome}."}, 404

    @jwt_required()
    def put(self, nome):
        dati = Oggetto.parser.parse_args()
        oggetto_esistente = next(filter(lambda oggetto: oggetto['name'] == nome, oggetti), None)

        if oggetto_esistente:
            oggetto_esistente.update(dati)
            return oggetto_esistente, 200
        else:
            nuovo_oggetto = {'nome': nome, 'prezzo': dati.get('prezzo', 0)}
            oggetti.append(nuovo_oggetto)
            return nuovo_oggetto, 201


class Oggetti(Resource):
    @jwt_required()
    def get(self):
        return {'oggetti': oggetti}


api.add_resource(Oggetto, '/oggetto/<string:nome>')
api.add_resource(Oggetti, '/oggetti')

if __name__ == '__main__':
    app.run()
