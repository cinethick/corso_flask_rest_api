from typing import Any, Optional, Mapping

from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage


class PercorsoFileStorage(fields.Field):
    default_error_messages = {
        "invalida": "Non è un immagine valida.",
    }

    def _deserialize(
        self,
        value: Any,
        attr: Optional[str],
        data: Optional[Mapping[str, Any]],
        **kwargs,
    ) -> Optional[FileStorage]:
        if value is None:
            return None

        if not isinstance(value, FileStorage):
            self.fail("invalida")  # genera un errore di validazione

        # qui potrebbe verificare il Mime type, il nome del file e l'estensione

        return value


class SchemaImmagine(Schema):
    immagine = PercorsoFileStorage(required=True)
