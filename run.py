'''this file is created for testing & deploying purpose'''
from db import db
from app import app

@app.before_first_request
def create_table():
    db.create_all()


db.init_app(app)


