import os

from requests import post, Response

MAILGUN = {
    "dominio": os.environ.get("MAILGUN_DOMINIO"),
    "apikey": os.environ.get("MAILGUN_APIKEY"),
    "utente": os.environ.get("MAILGUN_UTENTE"),
    "titolo": os.environ.get("MAILGUN_TITOLO"),
    "email": os.environ.get("MAILGUN_EMAIL"),
}


def invia_email(email: list[str], soggetto: str, testo: str, html: str) -> Response:
    return post(
        f"https://api.mailgun.net/v3/{MAILGUN['dominio']}/messages",
        auth=("api", MAILGUN["apikey"]),
        data={
            "from": f"{MAILGUN['titolo']} <{MAILGUN['email']}>",
            "to": email,
            "subject": soggetto,
            "text": testo,
            "html": html,
        },
    )
