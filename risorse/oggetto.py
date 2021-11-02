from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from modelli.oggetto import ModelloOggetto


class Oggetto(Resource):
    """
    Classe API oggetto
    """
    # Questo è una proprietà statica che appartiene alla classe e non all'istanza
    # Permette di fare il parsing delle proprietà dell'oggetto
    parser = reqparse.RequestParser()
    parser.add_argument(
        'prezzo',
        type=float,
        required=True,
        help="Questo campo non può essere lasciato vuoto"
    )
    parser.add_argument(
        'negozio_id',
        type=int,
        required=True,
        help="Ogni negozio deve avere l'id del proprio negozio"
    )

    @jwt_required()
    def get(self, nome: str):
        oggetto = ModelloOggetto.trova_per_nome(nome)
        if oggetto:
            return oggetto.json()
        return {'errore': 'Oggetto non trovato'}, 404

    @jwt_required()
    def post(self, nome: str):
        if ModelloOggetto.trova_per_nome(nome):
            return {'errore': f"E' già presente un oggetto chiamato {nome}."}, 409

        dati = Oggetto.parser.parse_args()
        nuovo_oggetto = ModelloOggetto(nome, dati['prezzo'], dati['negozio_id'])

        try:
            nuovo_oggetto.salva()
        except:
            return {'errore': 'Si è verificato un errore inserendo l\'oggetto'}, 500

        return nuovo_oggetto.json(), 201

    @jwt_required()
    def delete(self, nome):
        oggetto_esistente = ModelloOggetto.trova_per_nome(nome)
        if oggetto_esistente:
            try:
                oggetto_esistente.elimina()
            except:
                return {'errore': 'Si è verificato un errore eliminando l\'oggetto'}, 500

            return {'messaggio': 'Oggetto eliminato'}
        else:
            return {'errore': f"Non è presente un oggetto chiamato {nome}."}, 404

    @jwt_required()
    def put(self, nome):
        dati = Oggetto.parser.parse_args()
        oggetto = ModelloOggetto.trova_per_nome(nome)

        if oggetto:
            oggetto.prezzo = dati['prezzo']
            oggetto.negozio_id = dati['negozio_id']
            codice = 200
        else:
            oggetto = ModelloOggetto(nome, **dati)
            codice = 201

        try:
            oggetto.salva()
        except:
            return {'errore': 'Si è verificato un errore inserendo l\'oggetto'}, 500

        return oggetto.json(), codice


class Oggetti(Resource):
    @jwt_required()
    def get(self):
        return {'oggetti': [oggetto.json() for oggetto in ModelloOggetto.trova_tutti()]}
