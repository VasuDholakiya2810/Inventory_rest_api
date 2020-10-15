""" Validation for updating inventory input """
from marshmallow import Schema, fields


class InventoryUpdateSchema(Schema):
    inventory_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
