import os
from flask import g
from flask_oauthlib.client import OAuth

oauth = OAuth()

github = oauth.remote_app(
    "github",
    base_url="https://api.github.com",
    request_token_url=None,  # era per OAuth1
    request_token_params={"scope": "user-email"},
    access_token_method="POST",
    access_token_url="https://github.com/login/oauth/access_token",  # questo prende la nostra key e secret
    authorize_url="https://github.com/login/oauth/authorize",  # questo prende le richieste dei nostri utenti
    app_key="GITHUB",
)


@github.tokengetter
def prendi_github_tokengetter():
    if "access_token" in g:
        return g.access_token
