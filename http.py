import os.path
import socket
import logging
import struct
import threading


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Server:
    HOSTNAME = socket.gethostname()
    HOST = socket.gethostbyname(HOSTNAME)
    PORT = 80

    BUFFER = 512

    DEFAULT_PATH = "files"

    def __init__(self, server_files=None):
        self.FILES = server_files or self.DEFAULT_PATH

    def start(self):
        logging.info("[start] Starting server on %s:%d ...", self.HOST, self.PORT)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind((self.HOST, self.PORT))
                sock.listen(16)
                self.accept(sock)
        except socket.timeout:
            logging.error("[start] Connection timed out.")
        except socket.error as e:
            logging.error("[start] Socket error: %s", e)
            raise
        except Exception as e:
            logging.error("[start] Unexpected error: %s", e)
            raise

    def accept(self, sock):
        client_sock, client_addr = sock.accept()
        logging.info("[accept] %s successfully connected.", client_addr)
        self.get_request(client_sock)

    def map_request(self, request):
        lines = request.split("\r\n")
        method, path_with_query, version = lines[0].split(" ")

        if '?' in path_with_query:
            path, query_string = path_with_query.split('?', 1)
            query_params = {
                key: value for key, value in (param.split('=') for param in query_string.split('?'))
            }
        else:
            path = path_with_query
            query_params = {}

        headers = {}
        for line in lines[1:]:
            if line == "":
                break
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()

        body_index = lines.index("") + 1 if "" in lines else len(lines)
        body = "\n".join(lines[body_index:])

        return {
            "method": method,
            "path": path,
            "query_params": query_params,
            "headers": headers,
            "body": body,
        }

    def send_response(self, client, response):
        logging.info("[send_response] Sending response...")
        client.send(response.encode())

    def GET(self, client, request):
        requested_file_path = self.FILES.join(request['path'])
        if not os.path.exists(requested_file_path):
            client.send(b'')

    def get_request(self, client):
        request_data = client.recv(self.BUFFER).decode()
        print(request_data)
        request = self.map_request(request_data)

        match request["method"]:
            case 'GET':
                self.GET(client, request)
            case _:
                logging.info("[get_request] request method (%s) not available at the moment.", request["method"])

if __name__ == "__main__":
    server = Server()
    server.start()
