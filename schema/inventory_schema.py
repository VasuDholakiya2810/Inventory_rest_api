""" Validation for inserting and getting inventory """
from marshmallow import Schema, fields, validate


class InventoryDetail(Schema):
    inventory_id = fields.Int()
    inventory_name = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    inventory_category = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    is_expired = fields.Bool()
    quantity = fields.Int(required=True)
    img_url = fields.Str()
    expiry_date = fields.DateTime('%d-%m-%Y %H:%M:%z')
    manufacturing_date = fields.DateTime('%d-%m-%Y %H:%M:%z', required=True)

    load_only = (inventory_name, inventory_category, quantity, expiry_date, manufacturing_date)


class InventorySchema(Schema):
    ok = fields.Boolean(default=True)
    inventories = fields.List(fields.Nested(InventoryDetail), many=True)
