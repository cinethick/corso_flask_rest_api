from marshmallow import Schema, fields


class SchemaNegozio(Schema):
    class Meta:
        dump_only = ("id",)

    id = fields.Int()
    nome = fields.Str(required=True)
