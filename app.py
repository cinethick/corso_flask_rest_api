from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

oggetti = []


class Oggetto(Resource):
    """
    Classe API oggetto
    """
    def get(self, nome):
        oggetto_cercato = list(filter(lambda oggetto: oggetto['name'] == name, oggetti)).pop(0)
        # Si crea un oggetto filtro, si converte in lista
        # e si usa next( ..., None) per ritornare None se la lista è vuota
        return {'oggetti': oggetto_cercato}, 200 if oggetto_cercato else 404

    def post(self, nome):
        dati = request.get_json()
        oggetto = {'nome': nome, 'prezzo': dati.get('prezzo', 0)}
        oggetti.append(oggetto)
        return oggetto, 201


class Oggetti(Resource):
    def get(self):
        return {'oggetti': oggetti}


api.add_resource(Oggetto, '/oggetto/<string:nome>')
api.add_resource(Oggetti, '/oggetti')

if __name__ == '__main__':
    app.run()
