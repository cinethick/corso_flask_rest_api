"""
Classe utente dell'applicazione
"""
from dataclasses import dataclass


@dataclass
class Utente:
    """Classe che rappresenta un utente dell'applicazione"""
    id: int
    nome: str
    password: str
