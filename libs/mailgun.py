import os

from requests import post, Response

from libs.testi import prendi_testo

MAILGUN = {
    "dominio": os.environ.get("MAILGUN_DOMINIO"),
    "apikey": os.environ.get("MAILGUN_APIKEY"),
    "utente": os.environ.get("MAILGUN_UTENTE"),
    "titolo": os.environ.get("MAILGUN_TITOLO"),
    "email": os.environ.get("MAILGUN_EMAIL"),
}


class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def invia_email(email: list[str], soggetto: str, testo: str, html: str) -> Response:
    if MAILGUN["dominio"] is None:
        raise MailGunException(prendi_testo("mailgun_dominio"))

    if MAILGUN["apikey"] is None:
        raise MailGunException(prendi_testo("mailgun_apikey"))

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
            prendi_testo("mailgun_exception").format(
                soggetto, risposta.status_code, risposta.json()
            )
        )
    return risposta
