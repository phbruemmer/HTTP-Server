from backend.copy_files import copy
from backend import DEFAULTS

import os.path
import logging
import settings
import shutil


def copy_all_statics():
    """
    copies all static files including those that are included in previously added apps.
    :return:
    """
    logging.info("[copy_all_statics] copying static files.")
    if os.path.exists(settings.DEFAULT_STATIC_FILE_PATH):
        # Copies static files from the content root
        copy(settings.DEFAULT_STATIC_FILE_PATH, DEFAULTS.STATIC)
        logging.info("[copy_all_statics] root directory static file copied over to local static file directory.")

    for app in settings.apps:
        # Iterates through the settings.apps vector to get all allowed apps
        try:
            # Tries to copy static files from that current app
            origin = os.path.join(app, settings.DEFAULT_STATIC_FILE_PATH)
            destination = os.path.join(DEFAULTS.STATIC, app)
            copy(origin, destination)
            logging.info("[copy_all_statics] copied static files from %s to %s", origin, DEFAULTS.STATIC)
        except Exception as e:
            logging.error("[copy_all_statics] Unexpected error - Did you check your paths in settings.py? - %s", e)
            raise


def update_statics():
    """
    updates the locally saved static files directory to limit the access to the computer.
    Note that the DEFAULT.STATIC path is the local path and that the settings.DEFAULT_STATIC_FILE_PATH is
    the directory name / path to the static files that you created.
    :return:
    """
    if not os.path.exists(settings.DEFAULT_STATIC_FILE_PATH) or not os.path.exists(DEFAULTS.STATIC):
        logging.error("[update] No such path found.")
        raise
    try:
        for file in os.listdir(DEFAULTS.STATIC):
            # Iterates through all files in the default static directory
            file_path = os.path.join(DEFAULTS.STATIC, file)
            try:
                # removes all files and directories
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logging.error("[update] Unexpected error while removing static files: %s", e)
        # copies the new static files to the default static file directory
        copy_all_statics()
        logging.info("[update] successfully updated static file system.")
    except FileNotFoundError as e:
        logging.error("[update] Could not find file: %s", e)
        raise
    except Exception as e:
        logging.error("[update] Unkown error: %s", e)
        raise
