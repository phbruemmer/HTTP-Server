from backend import url_handler, error_handling, http_mapper
from backend.request_methods import GET
import socket
import logging
import threading

TXT_LOG = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Server:
    BUFFER = 8192

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
                thread = threading.Thread(target=self.handle_request, args=(client_sock,), daemon=True)
                thread.start()
            except socket.timeout:
                continue
            except OSError as e:
                logging.error("[accept] OSError - Likely due to socket closure: %s", e)
                break

    def send_response(self, client, response):
        """
        Sends http response to the client.
        :param client: client_sock
        :param response: generated http response from DEFAULTS function.
        :return:
        """
        logging.info("[send_response] Sending response...")
        client.send(response)

    def receive_request(self, client):
        data = b''
        while True:
            part = client.recv(self.BUFFER)
            data += part
            if len(part) < self.BUFFER:
                break
        return data.decode()

    def handle_request(self, client):
        """
        Handles HTTP requests.
        :param client: client_sock
        :return:
        """
        self.request_count += 1
        logging.info("[get_request] Request #%s being processed...", self.request_count)

        request_data = self.receive_request(client)

        try:
            request = http_mapper.map_request(request_data)
            match request["method"]:
                case 'GET':
                    response = GET.GET(self.HOST, request)
                case 'POST':
                    response = url_handler.handle(request)
                case _:
                    response = error_handling.render_error(self.HOST, 404)
                    logging.info("[get_request] request method (%s) not available at the moment.", request["method"])
            self.send_response(client, response)
        except Exception as e:
            logging.error("[start] Unexpected error: %s", e)
            logging.error("[start] Unexpected error: 500 Internal Server Error")
            response = error_handling.render_error(self.HOST, 500)
            self.send_response(client, response)
        finally:
            client.close()


if __name__ == '__main__':
    Server('192.168.115.200', 80).start_server()
