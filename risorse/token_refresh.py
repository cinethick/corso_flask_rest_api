from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_restful import Resource


class TokenRefresh(Resource):
    @jwt_required(fresh=True)
    def post(self):
        utente_corrente = get_jwt_identity()
        nuovo_token = create_access_token(identity=utente_corrente, fresh=True)
        return {"access_token": nuovo_token}, 200
