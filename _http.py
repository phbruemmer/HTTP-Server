import os.path
import socket
import logging
import threading

from backend import url_handler

import DEFAULTS


TXT_LOG = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Server:
    # HOSTNAME = socket.gethostname()
    # HOST = socket.gethostbyname(HOSTNAME)
    HOST = '0.0.0.0'
    PORT = 80

    BUFFER = 8192

    DEFAULT_PATH = "files/"
    LOG_FILE = "LOGS/HTTP_LOG.txt"

    def __init__(self, server_files=None):
        self.FILES = server_files or self.DEFAULT_PATH
        self.shutdown_event = threading.Event()
        self.lock = threading.Lock()
        self.request_count = 0

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
        finally:
            logging.error("[start] Shutting down server")
            self.stop_server(sock)

    def stop_server(self, sock):
        """
        Stops the server and closes the socket.
        :param sock: Socket Object
        :return:
        """
        logging.info("[stop_server] Shutting down server...")
        self.shutdown_event.set()
        sock.close()

    def accept(self, sock):
        """
        Accepts the connection from the client.
        :param sock: Socket from socket.socket(ipv4, TCP)
        :return:
        """
        while not self.shutdown_event.is_set():
            try:
                client_sock, client_addr = sock.accept()
                logging.info("[accept] %s successfully connected.", client_addr)
                threading.Thread(target=self.get_request, args=(client_sock,), daemon=True).start()
            except OSError as e:
                logging.info("[accept] OSError - Likely due to socket closure: %s", e)
                break

    def map_request(self, request):
        """
        Converts HTTP request to hashmap for better processing.
        :param request: HTTP request (string)
        :return: request hashmap / dictionary
        """
        try:
            lines = request.split("\r\n")
            method, path_with_query, version = lines[0].split(" ")
        except ValueError as e:
            logging.error("[map_request] Malformed request: %s", e)
            raise ValueError("Invalid HTTP request line.")

        query_params = {}

        if '?' in path_with_query:
            path, query_string = path_with_query.split('?', 1)
            for param in query_string.split('&'):
                arg = param.split('=')
                query_params[arg[0]] = arg[1]
        else:
            path = path_with_query

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
        :param request: request Hashmap with HTTP information
        :return:
        """
        if url_handler.check_urls(request['path']) and 'html' in request['headers']['Accept']:
            logging.info("[GET] Path found - 200 OK")
            response = url_handler.handle(request)
        elif 'css' in request['headers']['Accept']:
            logging.info("[GET] adding css - 200 OK")
            response = DEFAULTS.generate_response(200, self.HOST, os.path.join(self.DEFAULT_PATH, request['path'].lstrip('/')), True)
        else:
            logging.info("[GET] No such path found - 404 Not Found.")
            response = DEFAULTS.generate_response(404, self.HOST, os.path.join(self.DEFAULT_PATH, '404.html'), True)
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

        with self.lock:
            self.request_count += 1
            logging.info("[get_request] Request #%s being processed...", self.request_count)
            if TXT_LOG:
                with open(self.LOG_FILE, 'a') as log:
                    log.write(f'[Server] request #{self.request_count}:\n\n{request_data}\n')

        try:
            request = self.map_request(request_data)
            match request["method"]:
                case 'GET':
                    response = self.GET(request)
                    self.send_response(client, response)
                case 'POST':
                    response = url_handler.handle(request)
                    self.send_response(client, response)
                case _:
                    logging.info("[get_request] request method (%s) not available at the moment.", request["method"])
        except Exception as e:
            logging.error("[start] Unexpected error: %s", e)
            logging.error("[start] Unexpected error: 500 Internal Server Error")
            response_500 = DEFAULTS.generate_response(500, self.HOST, 'files/500.html', True)
            self.send_response(client, response_500)
        finally:
            client.close()
            with self.lock:
                logging.info("[get_request] finished processing request #%s", self.request_count)


if __name__ == "__main__":
    server = Server()
    server.start()
