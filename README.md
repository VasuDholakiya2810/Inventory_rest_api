# Inventory REST API

## Requirements
````
Python : 3+ version
Flask
Flask-RESTful
Flask-SQLAlchemy
Flask-SQLAlchemy
maya==0.6.1
pymysql
Python-dotenv
marshmallow
pytz
flask-Uploads
````
## Implemenattion
this REST API is implemented using Flask and Flask_SQLALchemy.this API is inventory management api.in this inserting,updating,deleting and fetching operation are available and all json payload input is validating through marshmallow and also serialization and deserialtion are performed.

## Endpoints

* Create Inventory: http://127.0.0.1:5000/inventory \
url for inserting inventory details. in which you have to enter inventory_name, inventory_category, quantity, expiry_date(optional) and manufacturing_date.

* Update Inventory: http://127.0.0.1:5000/inventory/update \
url for updating quantity of inventory in which you have to pass inventory_id and quantity(new quantity) for updating quantity. 

* Delete Inventory: http://127.0.0.1:5000/inventory/delete \
url for deleting multiple deleting inventories in which you have to pass inventory_name.

* Get Inventory: http://127.0.0.1:5000/inventory?inventory_name=something&category=something \
Url for getting inventories, you can also passing timezone.

* Create Category: http://127.0.0.1:5000/category/category_name \
url for creating category with category name.

* Upload Inventory Images: http://127.0.0.1:5000/image/upload/inventory_id \
url for uploading inventory with specified inventory_id.




````
Note:install requirements.txt using pip install -r requirements.txt command.
if ImportError: from werkzeug import secure_filename, FileStorage. occurred
then do following changes
in flask_uploads.py change from werkzeug.utils import secure_name and
from werkzeug.datastructures import FileStorage
````
