from db.gestione import database


class ModelloUtente(database.Model):
    """Classe che rappresenta un utente dell'applicazione"""
    __tablename__ = 'utenti'

    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(80))
    password = database.Column(database.String(80))

    def __init__(self, nome: str, password: str):
        self.nome = nome
        self.password = password

    @classmethod
    def trova_per_nome(cls, nome: str) -> "ModelloUtente":
        return cls.query.filter_by(nome=nome).first()

    @classmethod
    def trova_per_id(cls, _id: int) -> "ModelloUtente":
        return cls.query.filter_by(id=_id).first()

    def json(self) -> dict:
        return {"nome": self.nome, "password": self.password}

    def salva(self):
        database.session.add(self)
        database.session.commit()

    def elimina(self):
        database.session.delete(self)
        database.session.commit()
