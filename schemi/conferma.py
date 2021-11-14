from modelli.conferma import ModelloConferma
from schemi.validazione import validazione


class SchemaConferma(validazione.SQLAlchemyAutoSchema):
    class Meta:
        model = ModelloConferma
        load_only = ("utente",)
        dump_only = ("id", "scadenza", "confermata")
        include_relationships = True
        load_instance = True
