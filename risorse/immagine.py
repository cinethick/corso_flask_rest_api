from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from libs import gestione_immagini
from libs.testi import prendi_testo
from schemi.immagine import SchemaImmagine


schema_immagine = SchemaImmagine()


class UploadImmagine(Resource):
    @jwt_required()
    def post(self):
        """
        Si usa per fare l'upload del file.
        Usa il JWT per avere le informazioni sull'utente.
        Crea e gestisce una cartella per ogni utente.
        Gestisce conflitti nei nommi dei file
        """

        dati = schema_immagine.load(request.files)
        immagine = dati["immagine"]
        id_utente = get_jwt_identity()
        cartella = f"utente_{id_utente}"
        try:
            percorso_immagine = gestione_immagini.salva_immagini(immagine, cartella)
            nome_immagine = gestione_immagini.estrai_nome_file(percorso_immagine)
            return {
                "messaggio": prendi_testo("upload_immagine").format(nome_immagine)
            }, 201
        except UploadNotAllowed:
            estensione = gestione_immagini.estrai_estensione(immagine)
            return {
                "errore": prendi_testo("estensione_non_permessa").format(estensione)
            }, 400
