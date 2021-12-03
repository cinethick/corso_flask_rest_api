from collections import Counter

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from libs.testi import prendi_testo
from modelli.oggetto import ModelloOggetto
from modelli.ordine import ModelloOrdine, OggettiNellOrdine
from schemi.ordine import SchemaOrdine

schema_ordine = SchemaOrdine()


class Ordine(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        return schema_ordine.dump(ModelloOrdine.find_all(many=True))

    @classmethod
    @jwt_required(fresh=True)
    def post(cls):
        dati = request.get_json()
        oggetti = []
        errori = []
        quantita_id_oggetti = Counter(dati["id_oggetti"])

        for _id, quantita in quantita_id_oggetti.most_common():
            oggetto = ModelloOggetto.trova_per_id(_id)
            if not oggetto:
                errori.append(prendi_testo("oggetto_ordine_mancante").format(_id))
                continue
            oggetti.append(OggettiNellOrdine(id_oggetto=_id, quantita=quantita))

        if len(errori) > 0:
            return {
                "errore": prendi_testo("ordine_oggetti_mancanti"),
                "oggetti_mancanti": errori,
            }, 404

        ordine = ModelloOrdine(oggetti=oggetti, stato="in_corso")
        ordine.salva()

        ordine.imposta_stato("fallito")

        try:
            ordine.addebita_con_stripe(dati["token"])
            # Stripe ha una libreria per gli errori con dei template della gestione da implementare qui
        except Exception as err:
            print(err)
            return {
                "errore": prendi_testo("ordine_errore"),
            }, 500

        ordine.imposta_stato("completato")

        return schema_ordine.dump(ordine)
