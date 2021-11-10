from schemi.validazione import validazione
from modelli.oggetto import ModelloOggetto


class SchemaOggetto(validazione.SQLAlchemyAutoSchema):
    class Meta:
        model = ModelloOggetto
        load_only = ("negozio",)
        dump_only = ("id",)
        include_relationships = True
        load_instance = True
