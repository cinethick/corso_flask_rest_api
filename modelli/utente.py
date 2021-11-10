from db.gestione import database


class ModelloUtente(database.Model):
    """Classe che rappresenta un utente dell'applicazione"""

    __tablename__ = "utenti"

    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(80), nullable=False, unique=True)
    password = database.Column(database.String(500), nullable=False)

    @classmethod
    def trova_per_nome(cls, nome: str) -> "ModelloUtente":
        return cls.query.filter_by(nome=nome).first()

    @classmethod
    def trova_per_id(cls, _id: int) -> "ModelloUtente":
        return cls.query.filter_by(id=_id).first()

    def salva(self):
        database.session.add(self)
        database.session.commit()

    def elimina(self):
        database.session.delete(self)
        database.session.commit()
