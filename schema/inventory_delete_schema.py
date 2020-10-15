""" Validation for inventory delete input"""
from marshmallow import Schema, fields, validate


class InventoryDeleteSchema(Schema):
    inventory_name = fields.Str(required=True, validate=validate.Length(min=1, max=80))
