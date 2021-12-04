from flask import Blueprint, Response, render_template

blueprint = Blueprint("base", __name__, template_folder="templates")


@blueprint.route("/base")
def pagina_vista():
    return Response(render_template("principali/index.html"))
