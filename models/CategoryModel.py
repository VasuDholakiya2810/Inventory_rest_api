""" Mapping CategoryModel class to category table of daabase """
from db import db


class CategoryModel(db.Model):
    __tablename__ = "category"
    inventory_category = db.Column(db.String(80), primary_key=True)
    inventories = db.relationship('InventoryModel', lazy='dynamic')

    def __init__(self, inventory_category: str):
        self.inventory_category = inventory_category

    @classmethod
    def find_by_name(cls, category: str) -> "CategoryModel":
        """ :returns class Category object after applying filter"""
        
        return cls.query.filter_by(inventory_category=category).all()

    def save(self):
        """ save category in database """

        db.session.add(self)
        db.session.commit()
