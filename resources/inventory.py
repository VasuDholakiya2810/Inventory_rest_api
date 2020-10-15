""" Inventory Inventory, InventoryUpdate and InventoryDelete Resources."""
from flask import request, Response
from flask_restful import Resource
import maya
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models.InventoryModel import InventoryModel
from schema.inventory_schema import InventorySchema, InventoryDetail
from services.image_store import delete_image
from schema.inventory_update_schema import InventoryUpdateSchema
from schema.inventory_delete_schema import InventoryDeleteSchema
from common.logger_config import logger
from common.constant import (INSERTED_SUCCESSFULLY,
                             INTERNAL_SERVER_ERROR,
                             NO_ITEM_FOUND,
                             UPDATED_SUCCESSFULLY,
                             DELETED_SUCCESSFULLY,
                             CATEGORY_NOT_EXISTS
                             )

insert_schema = InventoryDetail()
get_schema = InventorySchema()
update_schema = InventoryUpdateSchema()
delete_schema = InventoryDeleteSchema()


class Inventory(Resource):
    """ Get and Post Inventory"""

    @classmethod
    def post(cls):
        request_data = request.get_json()
        try:
            data = insert_schema.load(request_data)

            logger.info('Parsing expiry date and converting into CTS timezone')
            expiry_date = data.get('expiry_date')
            manufacturing_date = maya.parse(data['manufacturing_date']).datetime(to_timezone='US/Central')
            if expiry_date:
                expiry_date = maya.parse(data['expiry_date']).datetime(
                    to_timezone='US/Central')

            logger.info('Inserting Inventory Data.')
            inventory_item = InventoryModel(data['inventory_name'], data['inventory_category'], data['quantity'],
                                            manufacturing_date, expiry_date)

            _id = inventory_item.insert()
            return {"message": INSERTED_SUCCESSFULLY, "Inventory_id": _id}, 201

        except IntegrityError as err:
            logger.error(err)
            return {"message": CATEGORY_NOT_EXISTS.format(request_data['inventory_category'])}, 404

        except ValidationError as err:
            return err.messages, 400

        except Exception as err:
            logger.error(err)
            return {"message": INTERNAL_SERVER_ERROR}, 500

    @classmethod
    def get(cls):
        try:
            name = request.args.get('inventory_name', type=str)
            category = request.args.get('category', type=str)
            timezone = request.args.get('timezone')

            if name and category:
                logger.info('Filtering data with Inventory Name and Category Parameter')
                inventory_list = InventoryModel.find_by_name_and_category(name, category)

                if inventory_list:
                    inventories = [inventory.check_expired(inventory.expiry_date, timezone) for inventory in
                                   inventory_list]
                    response_data = {"inventories": inventories}
                    return Response(InventorySchema().dumps(response_data), mimetype="application/json")

                return {"message": NO_ITEM_FOUND}, 404

            elif name:
                logger.info('Filtering data with name parameter')
                inventory_list = InventoryModel.find_by_name(name)
                if inventory_list:
                    inventories = [inventory.check_expired(inventory.expiry_date, timezone) for inventory in
                                   inventory_list]
                    response_data = {"inventories": inventories}
                    return Response(InventorySchema().dumps(response_data), mimetype="application/json")

                return {"message": NO_ITEM_FOUND}, 404

            elif category:
                logger.info('Filtering data with category parameter')
                inventory_list = InventoryModel.find_by_category(category)
                if inventory_list:
                    inventories = [inventory.check_expired(inventory.expiry_date, timezone) for inventory in
                                   inventory_list]
                    response_data = {"inventories": inventories}
                    return Response(InventorySchema().dumps(response_data), mimetype="application/json")

                return {"message": NO_ITEM_FOUND}, 404

            return {"message": NO_ITEM_FOUND}, 404

        except Exception as err:
            logger.error(err)
            return {"message": INTERNAL_SERVER_ERROR}, 500


class InventoryUpdate(Resource):
    """ Update Inventory"""

    @classmethod
    def put(cls):
        request_data = request.get_json()

        try:
            data = update_schema.load(request_data)

            logger.info('Updating Inventory Data')
            inventory = InventoryModel.find_by_id(data['inventory_id'])
            if inventory:
                inventory.quantity = data['quantity']
                logger.info('updating data to database.')
                inventory.insert()
                return {"message": UPDATED_SUCCESSFULLY}, 201

            return {"message": NO_ITEM_FOUND}, 404

        except ValidationError as err:
            return err.messages, 400

        except Exception as err:
            logger.error(err)
            return {"message": INTERNAL_SERVER_ERROR}, 500


class InventoryDelete(Resource):
    """ Delete Inventory """

    @classmethod
    def delete(cls):
        try:
            request_data = request.get_json()
            data = delete_schema.load(request_data)

            logger.info("Fetching Data")
            inventories = InventoryModel.find_by_name(data['inventory_name'])

            if inventories:
                for inventory in inventories:
                    logger.info('deleting data')
                    if inventory.img_url:
                        delete_image(inventory.img_url)
                    inventory.img_url = None
                    inventory.status = "deleted"
                    inventory.insert()

                return {"message": DELETED_SUCCESSFULLY.format(inventories[0].inventory_name)}, 200

            return {"message": NO_ITEM_FOUND}, 404

        except ValidationError as err:
            return err.messages, 400

        except Exception as e:
            logger.error(e)
            return {"message": INTERNAL_SERVER_ERROR}, 500
