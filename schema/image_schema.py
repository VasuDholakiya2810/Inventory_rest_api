""" Validation for image input """
from marshmallow import Schema, fields, ValidationError
from werkzeug.datastructures import FileStorage


class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "Not a valid image."
    }

    def _deserialize(self, value, attr, data, **kwargs) -> FileStorage:
        if value is None:
            return ValidationError("no image selected")

        if not isinstance(value, FileStorage):
            self.fail("invalid")

        return value


class ImageSchema(Schema):
    image = FileStorageField(required=True)
