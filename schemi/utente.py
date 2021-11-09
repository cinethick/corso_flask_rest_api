from marshmallow import Schema, fields


class SchemaUtente(Schema):
    class Meta:
        dump_only = ("id",)
        load_only = ("password",)

    id = fields.Int()
    nome = fields.Str(required=True)
    password = fields.Str(required=True)
