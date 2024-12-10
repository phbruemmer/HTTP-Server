import http_server
import socket
import sys


def main():
    arguments = sys.argv

    match arguments[1]:
        case 'runserver':
            HOST = socket.gethostbyname(socket.gethostname())
            PORT = 80
            if len(arguments) == 3:
                HOST, PORT = arguments[2].split(':')
            http_server.Server(HOST, int(PORT)).start_server()


if __name__ == '__main__':
    main()
