import os.path
import logging
from datetime import datetime
import mimetypes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

CODES = {
    200: '200 OK',
    404: '404 Not Found',
    500: '500 Internal Server Error',
    301: '301 Moved Permanently',
    302: '302 Found'
}


def generate_response(code, **kwargs):
    """
    Generate an HTTP response based on the status code, server name, and requested file path.
    :param code: The HTTP status Code (e.g. 200, 400).
    :param full_path: The full path to the file
    :param location: URL to redirect to.
    :param modified_file: In case the file was internally modified you can add new file content in here.
    :param close_connection: True: close || False: keep-alive
    :param server: The server name or identifier
    :return: A string representing the complete HTTP response
    """
    server = kwargs.get('server')
    full_path = kwargs.get('full_path')
    location = kwargs.get('location')
    modified_file = kwargs.get('modified_file')
    close_connection = kwargs.get('close_connection')

    current_time = datetime.now()
    formatted_time = current_time.strftime("%a, %d %b %Y %H:%M:%S GMT")

    if not os.path.isfile(full_path):
        logging.error(f"[generate_response] File not found: %s", full_path)
        raise FileNotFoundError(f"[generate_response] File not found: {full_path}")

    mime_type, _ = mimetypes.guess_type(full_path)
    content_type = mime_type or 'application/octet-stream'

    if modified_file is None:
        with open(full_path, 'rb') as file:
            file_content = file.read()
    else:
        file_content = modified_file.encode()

    file_size = len(file_content)

    http_location = ""

    if location:
        http_location += f"Location: {location}\r\n"

    headers = (f"HTTP/1.1 {CODES[code]}\r\n"
               f"Date: {formatted_time}\r\n"
               f"Server: {server}\r\n"
               f"{http_location}"
               f"Content-Type: {content_type}; charset=UTF-8\r\n"
               f"Connection: {'close' if close_connection else 'keep-alive'}\r\n"
               f"Content-Length: {file_size}\r\n\r\n")
    return headers + file_content.decode()


if __name__ == "__main__":
    print(generate_response(404, "Hans", 'files\\404.html', True))
