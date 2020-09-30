'''this file is contain all models which is connected to database table'''
from db import db
import os, maya
from datetime import datetime
import pytz
import logging

logger = logging.getLogger('InventoryApi.InventoryModel')


class InventoryModel(db.Model):
    __tablename__ = "inventory"
    logger.info('mapping objects with database table')
    inventory_id = db.Column(db.Integer, primary_key=True)
    inventory_name = db.Column(db.String(80))
    inventory_category = db.Column(db.String(80))
    quantity = db.Column(db.Integer)
    manufacturing_dt = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime, nullable=True)
    img_url = db.Column(db.String(150), nullable=True)
    status = db.Column(db.String(50))
    is_expired = db.Column(db.Boolean)

    def __init__(self, name, category, quantity, manufacturing_dt, expiry_date, img_url):
        self.inventory_name = name
        self.inventory_category = category
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.manufacturing_dt = manufacturing_dt
        self.img_url = img_url
        self.status = "Active"
        self.is_expired = False

    def json(self):
        return {"inventory_name": self.inventory_name, "category": self.inventory_category,
                "is_expired": self.is_expired,
                "expiry_date": str(self.expiry_date or "no expiry_date"), "quantity": self.quantity,
                "inventory_id": self.inventory_id, "image_path": self.img_url
                }

    @classmethod
    def find_by_name(cls, name):
        return [inventory for inventory in cls.query.filter_by(inventory_name=name, status="Active").all()]

    @classmethod
    def find_by_name_and_category(cls, name, category):
        return [inventory for inventory in
                cls.query.filter_by(inventory_name=name, inventory_category=category, status="Active").all()]

    @classmethod
    def find_by_category(cls, category):
        return [inventory for inventory in cls.query.filter_by(inventory_category=category, status="Active").all()]

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(inventory_id=_id, status="Active").first()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def image_save(cls, file):
        logger.info('save file in local system')
        root_path = "D:\\phase-2\\Task-2Img"
        path = '\\'.join([root_path, file.filename])
        file.save(path)
        return path

    @classmethod
    def delete_record(cls, path):
        logger.info('checking path/file is exists or not')
        if path and os.path.exists(path):
            os.remove(path)

    def check_expired(self, expiry_date, zone):
        logger.info('checking for expired inventories')
        if expiry_date:
            if zone:
                expiry = maya.parse(expiry_date).datetime()
                zone = pytz.timezone(zone)
                currenttime = zone.localize(datetime.now())
                if currenttime >= expiry:
                    self.is_expired = True
            else:
                currenttime = datetime.now()
                if currenttime >= expiry_date:
                    self.is_expired = True
        return self
