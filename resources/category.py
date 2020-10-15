""" Category Resource """
from flask_restful import Resource
from flask import Response

from models.CategoryModel import CategoryModel
from schema.category_schema import CategorySchema
from common.constant import CATEGORY_CREATED_SUCCESSFULLY, CATEGORY_ALREADY_EXISTS, CATEGORY_NOT_FOUND
from common.logger_config import logger


class Category(Resource):
    """ Category Resource """

    @classmethod
    def post(cls, inventory_category: str):
        logger.info('Check Category Exists or Not!')

        category = CategoryModel.find_by_name(inventory_category)
        if category:
            return {"message": CATEGORY_ALREADY_EXISTS.format(inventory_category)}, 400

        logger.info('Create Category')
        category = CategoryModel(inventory_category)
        category.save()
        return {"message": CATEGORY_CREATED_SUCCESSFULLY.format(inventory_category)}, 201

    @classmethod
    def get(cls, inventory_category: str):
        logger.info('Fetching Category')

        category = CategoryModel.find_by_name(inventory_category)
        if category:
            response_data = {"category": category}
            return Response(CategorySchema().dumps(response_data), mimetype="application/json")

        return {"message":CATEGORY_NOT_FOUND.format(inventory_category)},404

