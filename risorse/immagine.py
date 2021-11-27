import os
import traceback

from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request, send_file
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
            # evita di creare nomi dei file uguali a quelli esistenti per non sovrascrivere
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


class Immagine(Resource):
    @jwt_required()
    def get(self, nome_immagine: str):
        id_utente = get_jwt_identity()
        cartella = f"utente_{id_utente}"

        if gestione_immagini.nome_file_sicuro(nome_immagine):
            return {
                "errore": prendi_testo("nome_file_proibito").format(nome_immagine)
            }, 400

        try:
            return send_file(gestione_immagini.trova_immagine(nome_immagine, cartella))
        except FileNotFoundError:
            return {
                "errore": prendi_testo("file_non_trovato").format(nome_immagine)
            }, 404

    @jwt_required()
    def delete(self, nome_immagine: str):
        id_utente = get_jwt_identity()
        cartella = f"utente_{id_utente}"

        if gestione_immagini.nome_file_sicuro(nome_immagine):
            return {
                "errore": prendi_testo("nome_file_proibito").format(nome_immagine)
            }, 400

        try:
            os.remove(gestione_immagini.trova_immagine(nome_immagine, cartella))
            return {"messaggio": prendi_testo("immagine_eliminata")}, 200
        except FileNotFoundError:
            return {
                "errore": prendi_testo("file_non_trovato").format(nome_immagine)
            }, 404
        except:
            traceback.print_exc()
            return {"errore": prendi_testo("immagine_eliminazione")}, 500


class AvatarUpload(Resource):
    @jwt_required()
    def put(self):
        """
        Questa risorsa viene utilizzata per fare l'upload di un avatar utente.
        """
        dati = schema_immagine.load(request.files)
        immagine = dati["immagine"]
        id_utente = get_jwt_identity()
        nome_file = f"utente_{id_utente}"
        cartella = "avatars"
        percorso_avatar = gestione_immagini.trova_immagine(nome_file, cartella)

        if percorso_avatar:
            # elimina file esistente (anche con altra estensione)
            try:
                os.remove(percorso_avatar)
            except:
                traceback.print_exc()
                return {"errore": prendi_testo("immagine_eliminazione")}, 500

        try:
            estensione = gestione_immagini.estrai_estensione(immagine.filename)
            avatar = nome_file + estensione
            percorso_avatar = gestione_immagini.salva_immagini(
                immagine, cartella, avatar
            )
            nome_immagine = gestione_immagini.estrai_nome_file(percorso_avatar)
            return {
                "messaggio": prendi_testo("upload_immagine").format(nome_immagine)
            }, 201
        except UploadNotAllowed:
            estensione = gestione_immagini.estrai_estensione(immagine)
            return {
                "errore": prendi_testo("estensione_non_permessa").format(estensione)
            }, 400


class Avatar(Resource):
    @classmethod
    @jwt_required()
    def get(cls, id_utente: int):
        nome_file = f"utente_{id_utente}"
        cartella = "avatars"
        avatar = gestione_immagini.trova_immagine(nome_file, cartella)
        if avatar:
            return send_file(avatar)
        return {"errore": prendi_testo("file_non_trovato").format(nome_file)}, 404
