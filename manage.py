from backend import http_server, DEFAULTS
import os.path
import re
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


def update(arguments):
    """
    updates locally saved directories in the backend (e.g. static files)
    :param arguments:
    :return:
    """
    match arguments[2]:
        case 'statics':
            update_statics()


def runserver(arguments):
    """
    Starts the server using the IP and PORT given by the user (if no value it'll start on default settings)
    :param arguments:
    :return:
    """
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

    if len(arguments) < 1:
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
