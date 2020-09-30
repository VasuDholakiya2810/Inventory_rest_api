'''this file contains all resources and endpoints'''
from flask_restful import Resource, request
from models.InventoryModel import InventoryModel
import maya, json
import logging
logger=logging.getLogger('InventoryApi.InventoryResource')

class Inventory(Resource):
    ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF"]
    def post(self):
        try:
            logger.info('getting data from user request.')
            data = json.loads(request.form.get('data'))
            manufacturing_date = maya.parse(data['manufacturing_date']).datetime(to_timezone='US/Central')
            image = request.files.get('Image')
            extension=image.filename.split('.',1)[1]
            expiry_date = data.get('expiry_date', None)
            if image and extension.upper() in Inventory.ALLOWED_IMAGE_EXTENSIONS:
                path = InventoryModel.image_save(image)
            else:
                return {"message":'only image file allowed'},400
            logger.info('initialize data in InventoryModel')
            if expiry_date:
                expiry_date = maya.parse(data['expiry_date']).datetime(to_timezone='US/Central')
                inventory_item = InventoryModel(data['inventory_name'], data['inventory_category'], data['quantity'],
                                                manufacturing_date, expiry_date, path)
            else:
                inventory_item = InventoryModel(data['inventory_name'], data['inventory_category'], data['quantity'],
                                                manufacturing_date, expiry_date, path)

            inventory_item.insert()
            return {"message": "insert successfully", "image_path": path},201
        except Exception as e:
            logging.error(e)
            return {"message":"!!oops something went wrong"}, 503

    def put(self):
        try:
            logger.info('loading data from request.')
            data = json.loads(request.form.get('data'))
            logger.info("fetch relevant data from database")
            inventory = InventoryModel.find_by_id(data['id'])
            if inventory:
                inventory.quantity = data['quantity']
                logger.info('updating data to database.')
                inventory.insert()
                return {"message": "updated successfully"}
            return {"message": "no match found"},404
        except Exception as e:
            logger.error(e)
            return {"message":"!!oops something went wrong"},503

    def delete(self):
        try:
            logger.info('loading data from request.')
            data = json.loads(request.form['data'])
            logger.info("fetch relevant data from database")
            inventories = InventoryModel.find_by_name(data['inventory_name'])
            if inventories:
                for inventory in inventories:
                    logger.info('deleting data from database')
                    InventoryModel.delete_record(inventory.img_url)
                    inventory.img_url = None
                    inventory.status = "deleted"
                    inventory.insert()
                return {"message": "deleted successfully"}
            return {"message": "inventory not found"}, 404
        except Exception as e:
            logger.error(e)
            return {"message":"!!oops something went wrong"},503

    def get(self):
        name = request.args.get('inventory_name', type=str, default=0)
        category = request.args.get('category', type=str, default=0)
        timezone = request.args.get('timezone', default=0)
        if name and category:
            logger.info('filtering data with name and category parameter')
            inventories_list = InventoryModel.find_by_name_and_category(name, category)
            if inventories_list:
                inventories = [inventory.check_expired(inventory.expiry_date, timezone) for inventory in
                               inventories_list]

                return {"inventories": [inventory.json() for inventory in inventories]}
            return {"message": "no match found"}, 404

        elif name:
            logger.info('filtering data with name parameter')
            inventories_list = InventoryModel.find_by_name(name)
            if inventories_list:
                inventories = [inventory.check_expired(inventory.expiry_date, timezone) for inventory in
                               inventories_list]

                return {"inventories": [inventory.json() for inventory in inventories]}
            return {"message": "no match found"}, 404


        elif category:
            logger.info('filtering data with name parameter')
            inventories_list = InventoryModel.find_by_category(category)
            if inventories_list:
                inventories = [inventory.check_expired(inventory.expiry_date, timezone) for inventory in
                               inventories_list]

                return {"inventories": [inventory.json() for inventory in inventories]}
            return {"message": "no match found"}, 404

        return {"message": "no match found"}, 404
