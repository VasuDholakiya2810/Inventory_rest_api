""" Category Resource """
from flask_restful import Resource
from flask import Response

from models.CategoryModel import CategoryModel
from schema.category_schema import CategorySchema
from common.constant import CATEGORY_CREATED_SUCCESSFULLY, CATEGORY_ALREADY_EXISTS


class Category(Resource):
    @classmethod
    def post(cls, inventory_category: str):
        category = CategoryModel.find_by_name(inventory_category)
        if category:
            return {"message": CATEGORY_ALREADY_EXISTS.format(inventory_category)}, 400
        category = CategoryModel(inventory_category)
        category.save()
        return {"message": CATEGORY_CREATED_SUCCESSFULLY.format(inventory_category)}, 201

    @classmethod
    def get(cls, inventory_category: str):
        category = CategoryModel.find_by_name(inventory_category)
        print(category)
        if category:
            response_data = {"category": category}
            print(response_data)
            return Response(CategorySchema().dumps(response_data), mimetype="application/json")

