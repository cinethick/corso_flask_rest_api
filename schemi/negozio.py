from schemi.validazione import validazione
from schemi.oggetto import SchemaOggetto
from modelli.negozio import ModelloNegozio


class SchemaNegozio(validazione.SQLAlchemyAutoSchema):
    oggetti = validazione.Nested(SchemaOggetto, many=True)

    class Meta:
        model = ModelloNegozio
        dump_only = ("id", "oggetti")
        include_relationships = True
        load_instance = True
