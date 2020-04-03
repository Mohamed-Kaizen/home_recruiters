import importlib

from .settings import settings


def get_user_model():

    module_name, class_name = settings.User_MODEL.rsplit(".", 1)

    return getattr(importlib.import_module(module_name), class_name)


def get_model(*, data: str):

    module_name, class_name = data.rsplit(".", 1)

    return getattr(importlib.import_module(module_name), class_name)
