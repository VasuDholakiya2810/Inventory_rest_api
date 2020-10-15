""" Validation for Category inputs """
from marshmallow import Schema, fields

from schema.inventory_schema import InventorySchema


class CategorySchema(Schema):
    category = fields.List(fields.Nested(InventorySchema), many=True)
    include_fk = True
