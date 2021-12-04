import os

from flask import render_template, Response
from flask_restful import Resource


class Index(Resource):
    @classmethod
    def get(cls):
        pagina = {"titolo": os.getenv("MAILGUN_TITOLO")}
        return Response(render_template("principali/index.html", **pagina))
