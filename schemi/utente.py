from schemi.validazione import validazione
from modelli.utente import ModelloUtente


class SchemaUtente(validazione.SQLAlchemyAutoSchema):
    class Meta:
        model = ModelloUtente
        dump_only = ("id", "attivato")
        load_only = ("password",)
        load_instance = True
