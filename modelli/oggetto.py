from db.gestione import database
from modelli.ordine import OggettiNellOrdine


class ModelloOggetto(database.Model):
    """
    Modello che rappresenta un Oggetto nell'inventario dell'applicazione
    """

    __tablename__ = "oggetti"

    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(80), nullable=False, unique=True)
    prezzo = database.Column(database.Float(precision=2))

    # Relazione con altra tabella (padre)
    negozio_id = database.Column(
        database.Integer, database.ForeignKey("negozi.id"), nullable=False
    )
    negozio = database.relationship("ModelloNegozio", viewonly=True)
    ordini = database.relationship("OggettiNellOrdine", viewonly=True)

    @classmethod
    def trova_per_id(cls, _id: int) -> "ModelloOggetto":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def trova_per_nome(cls, nome: str) -> "ModelloOggetto":
        return cls.query.filter_by(nome=nome).first()

    @classmethod
    def trova_tutti(cls) -> list["ModelloOggetto"]:
        return cls.query.all()

    def salva(self):
        database.session.add(self)
        database.session.commit()

    def elimina(self):
        database.session.delete(self)
        database.session.commit()
