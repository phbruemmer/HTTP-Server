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
    418: "418 I'm a teapot",
    500: '500 Internal Server Error',
    301: '301 Moved Permanently',
    302: '302 Found',
}


def get_file_type(path):
    mime_type, _ = mimetypes.guess_type(path)
    content_type = mime_type or 'application/octet-stream'
    content_type = f"Content-Type: {content_type}; charset=UTF-8\r\n"
    return content_type


def check_path(path, modified_file):
    if not os.path.isfile(path):
        logging.error(f"[generate_response] File not found: %s", path)
        raise FileNotFoundError(f"[generate_response] File not found: {path}")
    if modified_file is None:
        with open(path, 'rb') as file:
            file_content = file.read()
    else:
        file_content = modified_file.encode()
    content_length = f"Content-Length: {len(file_content)}\r\n"
    return file_content, content_length


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

    file_content, content_length = check_path(full_path, modified_file) if full_path is not None else (b"", "")
    content_type = get_file_type(full_path) if full_path else ""

    http_location = f"Location: {location}\r\n" if location else ""

    headers = (f"HTTP/1.1 {CODES[code]}\r\n"
               f"Date: {formatted_time}\r\n"
               f"Server: {server}\r\n"
               f"{http_location}"
               f"{content_type}"
               f"Connection: {'close' if close_connection else 'keep-alive'}\r\n"
               f"{content_length}"
               f"\r\n")

    return headers + file_content.decode()


if __name__ == "__main__":
    print(generate_response(404, server="Hans", full_path='files\\404.html', close_connection=True))