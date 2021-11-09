from db.gestione import database


class ModelloNegozio(database.Model):
    """
    Modello che rappresenta un Negozio dell'applicazione
    """

    __tablename__ = "negozi"

    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(80), unique=True)

    # Relazione con altra tabella (figli)
    oggetti = database.relationship("ModelloOggetto", lazy="dynamic")

    def __init__(self, nome: str):
        self.nome = nome

    @classmethod
    def trova_per_nome(cls, nome) -> "ModelloNegozio":
        return cls.query.filter_by(nome=nome).first()

    @classmethod
    def trova_tutti(cls) -> list["ModelloNegozio"]:
        return cls.query.all()

    def salva(self):
        database.session.add(self)
        database.session.commit()

    def elimina(self):
        database.session.delete(self)
        database.session.commit()
