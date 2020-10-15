""" Inventory Image store """
import os

from flask_uploads import UploadSet, IMAGES
from werkzeug.datastructures import FileStorage

from common.logger_config import logger

IMAGE_SET = UploadSet("images", IMAGES)


def save_image(image: FileStorage, folder: str = None, name: str = None):
    logger.info('Save Image')

    return IMAGE_SET.save(image, folder, name)


def get_extension(filename):
    logger.info('Extension')

    return os.path.splitext(filename)[1]


def get_path(filename):
    logger.info('getting path')

    return IMAGE_SET.path(filename)


def delete_image(filename):
    logger.info('Deleting Image')

    path = get_path(filename)
    os.remove(path)
