import os.path
import http_server
import socket
import shutil
import settings
import logging
import sys


def update(args):
    match args[2]:
        case 'statics':
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

                for item in os.listdir(settings.DEFAULT_STATIC_FILE_PATH):
                    source_item = os.path.join(settings.DEFAULT_STATIC_FILE_PATH, item)
                    destination_item = os.path.join(STATIC, item)
                    if os.path.isdir(source_item):
                        shutil.copytree(source_item, destination_item)
                    else:
                        shutil.copy2(source_item, destination_item)
                logging.info("[update] successfully updated static file system.")
            except FileNotFoundError as e:
                logging.error("[update] Could not find file: %s", e)
                raise
            except Exception as e:
                logging.error("[update] Unkown error: %s", e)
                raise


def runserver(arguments):
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 80
    if len(arguments) == 3:
        HOST, PORT = arguments[2].split(':')
    http_server.Server(HOST, int(PORT)).start_server()


def main():
    arguments = sys.argv

    if not len(arguments) > 1:
        return

    match arguments[1]:
        case 'runserver':
            runserver(arguments)
        case 'update':
            update(arguments)


if __name__ == '__main__':
    main()
