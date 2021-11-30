from schemi.validazione import validazione
from modelli.oggetto import ModelloOggetto


class SchemaOggetto(validazione.SQLAlchemyAutoSchema):
    class Meta:
        model = ModelloOggetto
        load_only = ("negozio_id",)
        dump_only = ("id", "negozio", "ordini")
        include_relationships = True
        include_fk = True
        load_instance = True
