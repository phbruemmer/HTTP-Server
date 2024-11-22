import os.path
import socket
import logging
import threading
import time

import DEFAULTS


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Server:
    # bHOSTNAME = socket.gethostname()
    # HOST = socket.gethostbyname(HOSTNAME)
    HOST = '0.0.0.0'
    PORT = 80

    BUFFER = 8192

    DEFAULT_PATH = "files\\"

    def __init__(self, server_files=None):
        self.FILES = server_files or self.DEFAULT_PATH

    def start(self):
        """
        starts the HTTP server.
        :return: None
        """
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
        """
        Accepts the connection from the client.
        :param sock: Socket from socket.socket(ipv4, TCP)
        :return:
        """
        while True:
            client_sock, client_addr = sock.accept()
            logging.info("[accept] %s successfully connected.", client_addr)
            threading.Thread(target=self.get_request, args=(client_sock,), daemon=True).start()

    def map_request(self, request):
        """
        Converts HTTP request to hashmap for better processing.
        :param request: HTTP request (string)
        :return: request hashmap / dictionary
        """
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
        """
        Sends http response to the client.
        :param client: client_sock
        :param response: generated http response from DEFAULTS function.
        :return:
        """
        logging.info("[send_response] Sending response...")
        client.send(response.encode())

    def GET(self, request):
        """
        Handles GET method from the HTTP request.
        :param request: request Hashmap
        :return:
        """
        requested_file_path = os.path.join(self.DEFAULT_PATH, request['path'].lstrip('/'))
        if os.path.isfile(requested_file_path):
            logging.info("[GET] Path found - 200 OK")
            response = DEFAULTS.generate_response(200, self.HOST, os.path.join(requested_file_path), False)
        else:
            logging.info("[GET] No such path found - 404 Not Found.")
            response = DEFAULTS.generate_response(404, self.HOST, os.path.join(self.DEFAULT_PATH, '404.html'), False)
        return response

    def receive_request(self, client):
        data = b''
        while True:
            part = client.recv(self.BUFFER)
            data += part
            if len(part) < self.BUFFER:
                break
        return data.decode()

    def get_request(self, client):
        """
        HTTP request receiver.
        :param client: client_sock
        :return:
        """
        request_data = self.receive_request(client)
        try:
            request = self.map_request(request_data)
            match request["method"]:
                case 'GET':
                    response = self.GET(request)
                    self.send_response(client, response)
                case _:
                    logging.info("[get_request] request method (%s) not available at the moment.", request["method"])
        except Exception as e:
            logging.error("[start] Unexpected error: %s", e)
            logging.error("[start] Unexpected error: 500 Internal Server Error")
            response_500 = DEFAULTS.generate_response(500, self.HOST, 'files/500.html', False)
            self.send_response(client, response_500)
        finally:
            client.close()


if __name__ == "__main__":
    server = Server()
    server.start()
