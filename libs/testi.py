"""
libs.testi

Questa è una libreria per gestire la localizzazione dell'applicazione.
Di default utilizza il file 'it-it.json', che è posizionalto nella cartella 'testi'.

Per cambiare il linguaggio dell'applicazione bisogna:
  - assegnare il nuovo linguaggio come stringa a 'libs.testi.default_locale';
  - eseguire 'libs.testi.refresh()';
"""
import json
import traceback
from pathlib import Path

default_locale = "it-it"
cache_testi = {}


def leggi_json(file: Path) -> dict:

    if not file.exists():
        raise FileExistsError(f"Il file {str(file)} non è stato trovato!")

    if not file.is_file():
        raise FileNotFoundError(f"Il percorso {str(file)} non è un percorso!")

    if not file.suffix == ".json":
        raise TypeError(f"Il file {str(file)} non è del tipo json!")

    return json.loads(file.read_text(encoding="utf-8"))


def refresh(locale: str = default_locale):
    global cache_testi

    file_localizzazione = Path(f"./testi/{locale}.json")

    if not cache_testi:
        cache_testi = leggi_json(file_localizzazione)
    else:
        cache_testi = verifica_chiavi_testi(file_localizzazione)


def verifica_chiavi_testi(file_locale: Path):
    chiavi_iniziali = set(cache_testi.keys())
    nuovo_locale = leggi_json(file_locale)
    nuove_chiavi = set(nuovo_locale.keys())

    chiavi_mancanti = chiavi_iniziali - nuove_chiavi

    if chiavi_mancanti:
        testo_errore = f"Il file {str(file_locale)} non contiene le seguenti chiavi: ["
        for chiave in chiavi_mancanti:
            testo_errore = testo_errore + f"'{chiave}', "
        testo_errore = testo_errore[:-2] + "]"
        raise KeyError(testo_errore)

    return nuovo_locale


def prendi_testo(codice_messaggio: str):
    return cache_testi[codice_messaggio]


# Quando il file viene caricato esegue refresh() e carica cache_testi
refresh()
