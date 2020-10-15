""" Inventory Image store """
import os

from flask_uploads import UploadSet, IMAGES
from werkzeug.datastructures import FileStorage

IMAGE_SET = UploadSet("images", IMAGES)


def save_image(image: FileStorage, folder: str = None, name: str = None):
    return IMAGE_SET.save(image, folder, name)


def get_extension(filename):
    return os.path.splitext(filename)[1]


def get_path(filename):
    return IMAGE_SET.path(filename)


def delete_image(filename):
    path = get_path(filename)
    os.remove(path)
