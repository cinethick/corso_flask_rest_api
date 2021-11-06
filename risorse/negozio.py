from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from modelli.negozio import ModelloNegozio


class Negozio(Resource):
    """
    Classe API negozio
    """
    parser = reqparse.RequestParser()
    parser.add_argument(
        'nome',
        type=str,
        required=True,
        help="Questo campo non può essere lasciato vuoto"
    )

    @jwt_required()
    def get(self, nome: str):
        negozio = ModelloNegozio.trova_per_nome(nome)
        if negozio:
            return negozio.json()
        return {'errore': 'Negozio non trovato'}, 404

    @jwt_required()
    def post(self, nome: str):
        if ModelloNegozio.trova_per_nome(nome):
            return {'errore': f"E' già presente un negozio chiamato {nome}."}, 409

        nuovo_negozio = ModelloNegozio(nome)

        try:
            nuovo_negozio.salva()
        except:
            return {'errore': 'Si è verificato un errore inserendo il negozio'}, 500

        return nuovo_negozio.json(), 201

    @jwt_required()
    def delete(self, nome):
        negozio_esistente = ModelloNegozio.trova_per_nome(nome)
        if negozio_esistente:
            try:
                negozio_esistente.elimina()
            except:
                return {'errore': 'Si è verificato un errore eliminando il negozio'}, 500

            return {'messaggio': 'Negozio eliminato'}
        else:
            return {'errore': f"Non è presente un negozio chiamato {nome}."}, 404


class Negozi(Resource):
    @jwt_required(optional=True)
    def get(self):
        id_utente = get_jwt_identity()
        negozi = [negozio.json() for negozio in ModelloNegozio.trova_tutti()]
        if id_utente:
            return {"negozi": negozi}
        return {
            "oggetti": [negozio['nome'] for negozio in negozi],
            "messaggio": "I dati completi richiedono l'autenticazione"
        }, 200
