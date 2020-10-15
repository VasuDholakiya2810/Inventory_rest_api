""" all routes for endpoints are here."""

INSERT_INVENTORY = '/inventory'
UPDATE_INVENTORY = '/inventory/update'
DELETE_INVENTORY = '/inventory/delete'
INVENTORY_IMAGE_UPLOAD = '/inventory/image/upload/<int:inventory_id>'
CREATE_CATEGORY = '/category/<string:inventory_category>'
