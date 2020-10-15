""" Inventory Management RESTAPI """
from flask import Flask
from flask_restful import Api
import logging
from dotenv import load_dotenv
from flask_uploads import configure_uploads, patch_request_class

from resources.inventory import Inventory, InventoryUpdate, InventoryDelete
from resources.category import Category
from resources.image_upload import ImageUpload
from common.routes import CREATE_CATEGORY, DELETE_INVENTORY, INSERT_INVENTORY, INVENTORY_IMAGE_UPLOAD, UPDATE_INVENTORY
from services.image_store import IMAGE_SET

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s--%(levelname)-8s [%(filename)s:%(funcName)s:lineno:%(lineno)d]  %(message)s',
                    filename='logs.txt',
                    datefmt='%d-%m-%Y %H:%M:%S', filemode='w')

logger = logging.getLogger('InventoryApi')
app = Flask(__name__)
api = Api(app)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
patch_request_class(app, 5 * 1024 * 1024)
configure_uploads(app, IMAGE_SET)

api.add_resource(Inventory, INSERT_INVENTORY)
api.add_resource(InventoryUpdate, UPDATE_INVENTORY)
api.add_resource(InventoryDelete, DELETE_INVENTORY)
api.add_resource(ImageUpload, INVENTORY_IMAGE_UPLOAD)
api.add_resource(Category, CREATE_CATEGORY)

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    logger.info('Starting Inventory API')
    app.run()
