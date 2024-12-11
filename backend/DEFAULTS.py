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
    403: '403 Forbidden',
    404: '404 Not Found',
    418: "418 I'm a teapot",
    500: '500 Internal Server Error',
    301: '301 Moved Permanently',
    302: '302 Found',
}

STATIC = "backend/STATIC_FILES"


def get_file_type(path):
    mime_type, _ = mimetypes.guess_type(path)
    content_type = mime_type or 'application/octet-stream'
    content_type = f"Content-Type: {content_type}; charset=UTF-8\r\n"
    return content_type


def get_file_data(path):
    try:
        with open(path, 'rb') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        logging.error('[get_file_data] File not found %s', path)
        raise
    except PermissionError:
        logging.error('[get_file_data] Permission denied: %s', path)
        raise
    except Exception as e:
        logging.error('[get_file_data] Unexpected error with file %s: %s', (path, e))
        raise


def get_content_length(file_content):
    return f"Content-Length: {len(file_content)}\r\n"


def generate_response(code, **kwargs):
    """
    Generate an HTTP response based on the status code, server name, and requested file path.
    :param code: The HTTP status Code (e.g. 200, 400).
    :param server: The server name or identifier
    :param location: URL to redirect to.
    :param file_content: binary content of the file
    :param content_type: readable filetype of the HTTP response
    :param close_connection: True: close || False: keep-alive
    :return: A string representing the complete HTTP response
    """
    server = kwargs.get('server', 'Unkown Server')
    location = kwargs.get('location')
    file_content = kwargs.get('file_content', b'')
    content_type = kwargs.get('content_type', '')
    close_connection = kwargs.get('close_connection', True)
    cookie = kwargs.get('cookie', '')

    # # # # # # # # # # # # #
    # Checking for problems #
    # # # # # # # # # # # # #

    if code not in CODES:
        raise ValueError(f"[generate_response] Invalid HTTP status code: {code}")
    if file_content and not isinstance(file_content, bytes):
        raise TypeError("file_content must be of type bytes")

    current_time = datetime.now()
    formatted_time = current_time.strftime("%a, %d %b %Y %H:%M:%S GMT")

    headers = (f"HTTP/1.1 {CODES[code]}\r\n"
               f"Date: {formatted_time}\r\n"
               f"Server: {server}\r\n"
               f"{cookie}"
               f"{f"Location: {location}\r\n" if location else ""}"
               f"{content_type}"
               f"Connection: {'close' if close_connection else 'keep-alive'}\r\n"
               f"{get_content_length(file_content) if file_content else ""}"
               f"\r\n")
    return headers.encode() + file_content
