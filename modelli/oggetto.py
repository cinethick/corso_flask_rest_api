from db.gestione import database
from modelli.negozio import ModelloNegozio


class ModelloOggetto(database.Model):
    """
    Modello che rappresenta un Oggetto nell'inventario dell'applicazione
    """
    __tablename__ = 'oggetti'

    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(80))
    prezzo = database.Column(database.Float(precision=2))

    # Relazione con altra tabella (padre)
    negozio_id = database.Column(database.Integer, database.ForeignKey('negozi.id'))
    negozio = database.relationship("ModelloNegozio")

    def __init__(self, nome: str, prezzo: float, negozio_id: int):
        self.nome = nome
        self.prezzo = prezzo
        self.negozio_id = negozio_id

    @classmethod
    def trova_per_nome(cls, nome) -> "ModelloOggetto":
        return cls.query.filter_by(nome=nome).first()

    @classmethod
    def trova_tutti(cls):
        return cls.query.all()

    def json(self) -> dict:
        return {"nome": self.nome, "prezzo": self.prezzo}

    def salva(self):
        database.session.add(self)
        database.session.commit()

    def elimina(self):
        database.session.delete(self)
        database.session.commit()
