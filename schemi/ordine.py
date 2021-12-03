from modelli.ordine import ModelloOrdine
from schemi.validazione import validazione


class SchemaOrdine(validazione.SQLAlchemyAutoSchema):
    class Meta:
        model = ModelloOrdine
        load_only = ("token",)
        dump_only = ("id", "stato")
