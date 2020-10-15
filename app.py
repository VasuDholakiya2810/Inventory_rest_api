""" Inventory Management RESTAPI """
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from flask_uploads import configure_uploads, patch_request_class

from resources.inventory import Inventory, InventoryUpdate, InventoryDelete
from resources.category import Category
from resources.image_upload import ImageUpload
from common.routes import CREATE_CATEGORY, DELETE_INVENTORY, INSERT_INVENTORY, INVENTORY_IMAGE_UPLOAD, UPDATE_INVENTORY
from services.image_store import IMAGE_SET
from common.logger_config import logger

app = Flask(__name__)
api = Api(app)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
patch_request_class(app, 5 * 1024 * 1024)
configure_uploads(app, IMAGE_SET)


@app.before_first_request
def create_all_table():
    db.create_all()


api.add_resource(Inventory, INSERT_INVENTORY)
api.add_resource(InventoryUpdate, UPDATE_INVENTORY)
api.add_resource(InventoryDelete, DELETE_INVENTORY)
api.add_resource(ImageUpload, INVENTORY_IMAGE_UPLOAD)
api.add_resource(Category, CREATE_CATEGORY)

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    logger.info('Started api')
    app.run()
