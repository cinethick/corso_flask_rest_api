import os
import re
from typing import Union

from flask_uploads import UploadSet, IMAGES
from werkzeug.datastructures import FileStorage

SET_IMMAGINI = UploadSet("immagini", IMAGES)


def salva_immagini(
    immagine: FileStorage, percorso: str = None, nome: str = None
) -> str:
    """
    Prende FileStorage e lo salva in una cartella
    """
    return SET_IMMAGINI.save(immagine, percorso, nome)


def estrai_percorso(nome: str = None, percorso: str = None) -> str:
    """
    Prende il nome di un file e ritorna il percorso completo
    """
    return SET_IMMAGINI.path(nome, percorso)


def trova_immagine(nome_no_est: str, percorso: str) -> Union[str, None]:
    """
    Prende il nome di un file e restituisce un immagine in un formato specifico
    """
    for _format in IMAGES:
        # non sicuro... controllare mime
        immagine = f"{nome_no_est}.{_format}"
        percorso_immagine = SET_IMMAGINI.path(immagine, percorso)
        if os.path.isfile(percorso_immagine):
            return percorso_immagine
    return None


def _recupera_nome_file(file: Union[str, FileStorage]) -> str:
    """
    Prende un FileStorage e ritorna il nome del file
    """
    if isinstance(file, FileStorage):
        return file.filename
    return file


def nome_file_sicuro(file: Union[str, FileStorage]) -> bool:
    """
    Verifica che il nome del file corrisponda ad una regex
    """
    nome_file = _recupera_nome_file(file)

    formati_permessi = "|".join(IMAGES)
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({formati_permessi})$"

    return re.match(regex, nome_file) is not None


def estrai_nome_file(file: Union[str, FileStorage]) -> str:
    """
    Ritorna il nome base del file
    """
    nome_file = _recupera_nome_file(file)
    return os.path.split(nome_file)[1]


def estrai_estensione(file: Union[str, FileStorage]) -> str:
    """
    Ritorna l'estensione del file
    """
    nome_file = _recupera_nome_file(file)
    return os.path.splitext(nome_file)[1]
