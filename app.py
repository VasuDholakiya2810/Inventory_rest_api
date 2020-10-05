from flask import Flask
from flask_restful import Api
from resources.inventory import Inventory
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s--%(levelname)-8s [%(filename)s:%(funcName)s:lineno:%(lineno)d]  %(message)s',
                    filename='logs.txt',
                    datefmt='%d-%m-%Y %H:%M:%S', filemode='w')

logger = logging.getLogger('InventoryApi')



app=Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:@localhost/inventory"
app.config['PROPAGATE_EXCEPTION']=True
app.secret_key="something"

api.add_resource(Inventory,'/inventory')

if __name__=="__main__":
    from db import db
    db.init_app(app)
    logger.info('Starting Inventory API')
    app.run(debug=True)
