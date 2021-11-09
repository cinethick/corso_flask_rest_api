from marshmallow import Schema, fields


class SchemaOggetto(Schema):
    class Meta:
        load_only = ("id",)

    id = fields.Int()
    nome = fields.Str()
    prezzo = fields.Float()
    negozio_id = fields.Int()
