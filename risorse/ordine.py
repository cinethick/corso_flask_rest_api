from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from libs.testi import prendi_testo
from modelli.oggetto import ModelloOggetto
from modelli.ordine import ModelloOrdine


class Ordine(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def post(cls):
        dati = request.get_json()
        oggetti = []
        errori = []

        for _id in dati["id_oggetti"]:
            oggetto = ModelloOggetto.trova_per_id(_id)
            if not oggetto:
                errori.append(prendi_testo("oggetto_ordine_mancante").format(_id))
                continue
            oggetti.append(oggetto)

        if len(errori) > 0:
            return {
                "errore": prendi_testo("ordine_oggetti_mancanti"),
                "oggetti_mancanti": errori,
            }, 404

        ordine = ModelloOrdine(oggetti=oggetti, stato="pending")
        ordine.salva()
