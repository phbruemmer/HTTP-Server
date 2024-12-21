from backend.static_file_handling.static_file_handler import update_statics
from backend.app_handling.app_handler import add_app
from backend import http_server

import logging
import socket


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


def main(arguments):

    if len(arguments) < 1:
        return

    match arguments[1]:
        case 'runserver':
            runserver(arguments)
        case 'update':
            update(arguments)
        case 'add':
            add(arguments)
