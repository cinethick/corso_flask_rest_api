from flask_restful import Resource
from libs.oauth import github


class LoginGitHub(Resource):
    @classmethod
    def get(cls):
        return github.authorize(
            callback="http://localhost:5000/login/github/authorized"
        )
