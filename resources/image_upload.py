""" Inventory ImageUpload Resource """
from flask_uploads import UploadNotAllowed
from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
import os

from schema.image_schema import ImageSchema
from services import image_store
from models.InventoryModel import InventoryModel
from common.logger_config import logger
from common.constant import (
    INTERNAL_SERVER_ERROR,
    IMAGE_PATH,
    IMAGE_ALREADY_EXISTS,
    NO_ITEM_FOUND,
    NOT_VALID_EXTENSION
)


image_schema = ImageSchema()


class ImageUpload(Resource):
    """ ImageUpload Resource"""

    @classmethod
    def post(cls, inventory_id: int):
        request_image = request.files

        try:
            logger.info('Fetching Inventory')
            inventory = InventoryModel.find_by_id(inventory_id)
            if inventory:
                if inventory.img_url:
                    return {"message": IMAGE_ALREADY_EXISTS}, 400
                image = image_schema.load(request_image)
                logger.info('Saving Image')
                image_name = image_store.save_image(image['image'])
                inventory.img_url = image_name
                inventory.insert()
                path = os.path.join(IMAGE_PATH, image_name)
                return {"image_path": path}, 201

            return {"message": NO_ITEM_FOUND}, 404

        except ValidationError as err:
            return err.messages, 400

        except UploadNotAllowed:
            extension = image_store.get_extension(request_image['image'].filename)
            return {"message": NOT_VALID_EXTENSION.format(extension)}, 400

        except Exception as err:
            logger.error(err)
            return {"message": INTERNAL_SERVER_ERROR}, 500
