import os.path
import logging
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

CODES = {
    200: '200 OK',
    404: '404 Not Found',
}


def generate_response(code, server, full_path):
    """
    Generate an HTTP response based on the status code, server name, and requested file path.
    :param code: The HTTP status Code (e.g. 200, 400).
    :param server: The server name or identifier
    :param full_path: The full path to the file
    :return: A string representing the complete HTTP response
    """
    current_time = datetime.now()
    formatted_time = current_time.strftime("%a, %d %b %Y %H:%M:%S GMT")

    if not os.path.isfile(full_path):
        logging.error(f"[generate_response] File not found: %s", full_path)
        raise
    file_size = os.path.getsize(full_path)

    with open(full_path, 'r') as file:
        file_content = file.read()

    return (f"HTTP/1.1 {CODES[code]}\r\n"
            f"Date: {formatted_time}\r\n"
            f"Server: {server}\r\n"
            f"Content-Type: text/html; charset=UTF-8\r\n"
            f"Content-Length: {file_size}\r\n\n"
            f"{file_content}")

