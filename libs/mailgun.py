import os

from requests import post, Response

MAILGUN = {
    "dominio": os.environ.get("MAILGUN_DOMINIO"),
    "apikey": os.environ.get("MAILGUN_APIKEY"),
    "utente": os.environ.get("MAILGUN_UTENTE"),
    "titolo": os.environ.get("MAILGUN_TITOLO"),
    "email": os.environ.get("MAILGUN_EMAIL"),
}

MESSAGGI_MAILGUN = {
    "dominio": "Non è stato possibile caricare il dominio MailGun.",
    "apikey": "Non è stato possibile caricare la api key di MailGun.",
}


class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def invia_email(email: list[str], soggetto: str, testo: str, html: str) -> Response:
    if MAILGUN["dominio"] is None:
        raise MailGunException(MESSAGGI_MAILGUN["dominio"])

    if MAILGUN["apikey"] is None:
        raise MailGunException(MESSAGGI_MAILGUN["apikey"])

    risposta = post(
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

    if risposta.status_code != 200:
        raise MailGunException(
            f"Errore nell'invio della email ({soggetto}): status_code={risposta.status_code}, {risposta.json()}"
        )
    return risposta
