import os.path
import logging
import shutil


def copy(origin, destination):
    """
    responsible for copying files from origin to destination.
    :param origin: string -> origin path
    :param destination: string -> destination path
    :return:
    """
    if not os.path.exists(origin):
        logging.error("[copy] Can not copy from or to unknown locations.")
        return
    elif not os.path.exists(destination):
        logging.info("[copy] created new directory - %s", destination)
        os.makedirs(destination)
    try:
        for item in os.listdir(origin):
            source_item = os.path.join(origin, item)
            destination_item = os.path.join(destination, item)
            if os.path.isdir(source_item):
                shutil.copytree(source_item, destination_item)
            else:
                shutil.copy2(source_item, destination_item)
    except Exception as e:
        logging.error("[copy] Unexpected error: %s", e)
        raise
