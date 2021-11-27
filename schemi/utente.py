from marshmallow import pre_dump

from schemi.validazione import validazione
from modelli.utente import ModelloUtente


class SchemaUtente(validazione.SQLAlchemyAutoSchema):
    class Meta:
        model = ModelloUtente
        dump_only = ("id", "conferme")
        load_only = ("password",)
        load_instance = True

    @pre_dump
    def prima_del_dump(self, utente: ModelloUtente, **kwargs):
        utente.conferme = [utente.conferma_piu_recente]
        return utente
