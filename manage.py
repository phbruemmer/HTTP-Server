import os.path
import re
import http_server
import socket
import shutil
import settings
import logging
import sys


def clean_name(function):
    def wrapper(*args):
        name = re.sub('[^A-Za-z0-9]+', '', str(args[0]))
        function(name=name, arguments=args)

    return wrapper


def copy(origin, destination):
    for item in os.listdir(origin):
        source_item = os.path.join(origin, item)
        destination_item = os.path.join(destination, item)
        if os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item)
        else:
            shutil.copy2(source_item, destination_item)


def update_statics():
    STATIC = "backend/STATIC_FILES"
    if not os.path.exists(settings.DEFAULT_STATIC_FILE_PATH) or not os.path.exists(STATIC):
        logging.error("[update] No such path found.")
        raise
    try:
        for file in os.listdir(STATIC):
            file_path = os.path.join(STATIC, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception:
                logging.error("[update] Unexpected error while removing static files.")
        copy(settings.DEFAULT_STATIC_FILE_PATH, STATIC)
        logging.info("[update] successfully updated static file system.")
    except FileNotFoundError as e:
        logging.error("[update] Could not find file: %s", e)
        raise
    except Exception as e:
        logging.error("[update] Unkown error: %s", e)
        raise


@clean_name
def add_app(**kwargs):
    NEW_APP_PATH = kwargs.get('name')
    DEFAULT_VIEW_PATH = "backend/view_template"

    if os.path.exists(NEW_APP_PATH):
        logging.error("[add_app] Can not overwrite existing apps. Delete or choose a new name for your app.")
        return
    try:
        os.mkdir(NEW_APP_PATH)
        copy(DEFAULT_VIEW_PATH, NEW_APP_PATH)
        logging.info("[update] successfully added new app.")
    except Exception as e:
        logging.error("[add_app] Unexpected error: %s", e)
        raise


def update(arguments):
    match arguments[2]:
        case 'statics':
            update_statics()


def runserver(arguments):
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 80
    if len(arguments) == 3:
        HOST, PORT = arguments[2].split(':')
    http_server.Server(HOST, int(PORT)).start_server()


def add(arguments):
    match arguments[2]:
        case 'app':
            if not len(arguments) == 4:
                logging.error("[add] Can not add an app without a name.")
                return
            add_app(arguments[3])


def main():
    arguments = sys.argv

    if not len(arguments) > 1:
        return

    match arguments[1]:
        case 'runserver':
            runserver(arguments)
        case 'update':
            update(arguments)
        case 'add':
            add(arguments)


if __name__ == '__main__':
    main()
