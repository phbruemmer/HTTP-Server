from backend.decorators.clean_data import clean_name
from backend.copy_files import copy

import os.path
import logging


@clean_name
def add_app(**kwargs):
    """
    Adds app to the content root.
    This function copies the app_template directory into the content root directory (with a different name)
    :param kwargs:
    :return:
    """
    NEW_APP_PATH = kwargs.get('name')
    DEFAULT_APP_PATH = "backend/app_template"

    if os.path.exists(NEW_APP_PATH):
        logging.error("[add_app] Can not overwrite existing apps. Delete or choose a new name for your app.")
        return
    try:
        # creates new directory
        os.mkdir(NEW_APP_PATH)
        # copies files from the DEFAULT_APP_PATH
        copy(DEFAULT_APP_PATH, NEW_APP_PATH)
        logging.info("[update] successfully added new app.")
    except Exception as e:
        logging.error("[add_app] Unexpected error: %s", e)
        raise
