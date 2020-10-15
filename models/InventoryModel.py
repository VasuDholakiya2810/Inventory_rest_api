""" Mapping InventoryModel class with inventory table of database """
import maya
from datetime import datetime
import pytz
from typing import List

from db import db



class InventoryModel(db.Model):
    __tablename__ = "inventory"

    inventory_id = db.Column(db.Integer, primary_key=True)
    inventory_name = db.Column(db.String(80))
    inventory_category = db.Column(db.String(80), db.ForeignKey('category.inventory_category'))
    category = db.relationship('CategoryModel')
    quantity = db.Column(db.Integer)
    manufacturing_dt = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime, nullable=True)
    img_url = db.Column(db.String(150), nullable=True, default=None)
    status = db.Column(db.String(50), default="Active")
    is_expired = db.Column(db.Boolean, default=False)

    def __init__(self, name: str, category: str, quantity: str, manufacturing_dt: datetime, expiry_date: datetime):
        self.inventory_name = name
        self.inventory_category = category
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.manufacturing_dt = manufacturing_dt

    @classmethod
    def find_by_name(cls, inventory_name: str) -> List['InventoryModel']:
        """ :returns InventoryModel class object after applying filter by name """

        return [inventory for inventory in cls.query.filter_by(inventory_name=inventory_name, status="Active").all()]

    @classmethod
    def find_by_name_and_category(cls, inventory_name: str, inventory_category: str) -> List['InventoryModel']:
        """ :returns InventoryModel class object after applying filter by name and category """

        return [inventory for inventory in
                cls.query.filter_by(inventory_name=inventory_name, inventory_category=inventory_category,
                                    status="Active").all()]

    @classmethod
    def find_by_category(cls, inventory_category: str) -> List['InventoryModel']:
        """ :returns InventoryModel class object after applying filter by category"""

        return [inventory for inventory in
                cls.query.filter_by(inventory_category=inventory_category, status="Active").all()]

    @classmethod
    def find_by_id(cls, _id: int) -> "InventoryModel":
        """ :returns InventoryModel class object after applying filter by inventory_id """

        return cls.query.filter_by(inventory_id=_id, status="Active").first()

    def insert(self) -> "InventoryModel.inventory_id":
        """ insert inventory into database"""

        db.session.add(self)
        db.session.commit()
        return self.inventory_id

    def check_expired(self, expiry_date, zone) -> "InventoryModel":
        """ check inventory expired or not!!"""

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
