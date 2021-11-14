"""
libs.testi

Questa è una libreria per gestire la localizzazione dell'applicazione.
Di default utilizza il file 'it-it.json', che è posizionalto nella cartella 'testi'.

Per cambiare il linguaggio dell'applicazione bisogna:
  - assegnare il nuovo linguaggio come stringa a 'libs.testi.default_locale';
  - eseguire 'libs.testi.refresh()';
"""
import json
from pathlib import Path

default_locale = "it-it"
cache_testi = {}


def refresh():
    global cache_testi
    file_localizzazione = Path(f"./testi/{default_locale}.json")

    if not file_localizzazione.exists() or not file_localizzazione.is_file():
        raise FileNotFoundError(
            f"Il file di localizzazione {str(file_localizzazione)} non è stato trovato!"
        )

    cache_testi = json.loads(file_localizzazione.read_text(encoding="utf-8"))


def prendi_testo(codice_messaggio: str):
    return cache_testi[codice_messaggio]


# Quando il file viene caricato esegue refresh() e carica cache_testi
refresh()
