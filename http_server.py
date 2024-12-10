from backend import url_handler, error_handling, DEFAULTS

import os.path
import socket
import logging
import threading

import settings

TXT_LOG = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Server:
    BUFFER = 8192

    DEFAULT_PATH = settings.DEFAULT_PATH

    LOG_FILE = "LOGS/HTTP_LOG.txt"

    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.shutdown_event = threading.Event()
        self.lock = threading.Lock()
        self.request_count = 0
        self.server_thread = None

    def start_server(self):
        """
        starts the HTTP server.
        :return: None
        """
        logging.info("[start] Starting server on %s:%d ...", self.HOST, self.PORT)
        sock = None
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind((self.HOST, self.PORT))
                sock.listen(16)
                self.accept(sock)
        except socket.timeout:
            logging.error("[start] Connection timed out.")
            raise
        except socket.error as e:
            logging.error("[start] Socket error: %s", e)
            raise
        except KeyboardInterrupt:
            logging.info("[start_server] Keyboard Interrupt - Shutting down server.")
            self.stop_server(sock)
        except Exception as e:
            logging.error("[start] Unexpected error: %s", e)
            raise
        finally:
            logging.info("[start] Server offline.")

    def stop_server(self, sock):
        """
        Gracefully stops the server and closes all resources.
        :param sock: Server socket
        :return: None
        """
        logging.info("[stop_server] Initiating server shutdown...")
        self.shutdown_event.set()
        sock.close()
        logging.info("[stop_server] Server socket closed.")
        if self.server_thread is not None:
            self.server_thread.join()
            logging.info("[stop_server] Server thread joined.")
        logging.info("[stop_server] Server shut down gracefully.")

    def accept(self, sock):
        """
        Accepts connections from clients and starts a new thread to handle each connection.
        :param sock: Socket from socket.socket(ipv4, TCP)
        :return: None
        """
        while not self.shutdown_event.is_set():
            try:
                sock.settimeout(1.0)
                client_sock, client_addr = sock.accept()
                logging.info("[accept] %s successfully connected.", client_addr)
                thread = threading.Thread(target=self.get_request, args=(client_sock,), daemon=True)
                thread.start()
            except socket.timeout:
                continue
            except OSError as e:
                logging.error("[accept] OSError - Likely due to socket closure: %s", e)
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
        client.send(response)

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
            """
            UNSAFE CSS HANDLING
            """
            logging.info("[GET] adding css - 200 OK")
            path = os.path.join(self.DEFAULT_PATH, request['path'].lstrip('/'))
            file_content = DEFAULTS.get_file_data(path)
            content_type = DEFAULTS.get_file_type(path)
            response = DEFAULTS.generate_response(200, server=self.HOST, file_content=file_content,
                                                  content_type=content_type)
        else:
            logging.info("[GET] No such path found - 404 Not Found.")
            response = error_handling.render_error(self.HOST, 404)
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
            response = error_handling.render_error(self.HOST, 500)
            self.send_response(client, response)
        finally:
            client.close()
            with self.lock:
                logging.info("[get_request] finished processing request #%s", self.request_count)


if __name__ == '__main__':
    Server('192.168.115.200', 80).start_server()
