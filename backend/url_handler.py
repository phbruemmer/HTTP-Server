from backend import DEFAULTS, router
import logging
import settings
import os.path
import urls


def clean_path(function):
    """
    This decorator function cleans paths given from an HTTP request.
    Normally only used when handling static files, like css or js.
    it returns the requested path after removing all unnecessary characters from the path.
    :param function:
    :return:
    """

    def wrapper(request):
        # account/static_files/'css/index.css' (example)
        # the 'css/index.css' is the real path from the HTML
        requested_path = request['path'].lstrip('/')

        requested_path = requested_path.split(settings.DEFAULT_STATIC_FILE_PATH)  # ['account'], ["'css/index.css'"]
        requested_path = requested_path[1].replace("'", "").replace('"', '')      # css/index.css
        file_path = os.path.join(DEFAULTS.STATIC, requested_path)                 # STATIC_FILES/css/index.css
        return function(file_path)

    return wrapper


def handle(request):
    """
    Handles the url routing across the apps.
    :param request:
    :return:
    """
    return router.Router(urls.URL_PATTERNS).resolve(request['path'], request)


@clean_path
def get_statics(file_path):
    """
    Checks if the given file path is in the DEFAULT STATIC file path and if the file path even refers to a file.
    returns the file path (cleaned up with the clean_path decorator) if everything is OK, otherwise it returns None.
    :param file_path:
    :return:
    """
    try:
        if os.path.abspath(file_path).startswith(os.path.abspath(DEFAULTS.STATIC)) and os.path.isfile(file_path):
            return file_path
    except Exception as e:
        logging.error("[handle_statics] Unexpected error: %s", e)
        raise
    return None


def handle_statics(host, path):
    """
    parses important information about the file for the HTTP response generator
    and returns the generated response.
    :param host:
    :param path:
    :return:
    """
    file_content = DEFAULTS.get_file_data(path)
    content_type = DEFAULTS.get_file_type(path)
    response = DEFAULTS.generate_response(200,
                                          server=host,
                                          file_content=file_content,
                                          content_type=content_type)
    return response
