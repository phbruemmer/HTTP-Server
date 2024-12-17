from backend import DEFAULTS, router
import logging
import settings
import os.path
import urls


def clean_path(function):
    def wrapper(request):
        requested_path = request['path'].lstrip('/')
        requested_path = requested_path.split(settings.DEFAULT_STATIC_FILE_PATH)
        requested_path = requested_path[1].replace("'", "").replace('"', '')
        file_path = os.path.join(DEFAULTS.STATIC, requested_path)
        return function(file_path)
    return wrapper


def handle(request):
    return router.Router(urls.URL_PATTERNS).resolve(request['path'], request)


@clean_path
def get_statics(file_path):
    try:
        if os.path.abspath(file_path).startswith(os.path.abspath(DEFAULTS.STATIC)) and os.path.isfile(file_path):
            return file_path
    except Exception as e:
        logging.error("[handle_statics] Unexpected error: %s", e)
        raise
    return None


def handle_statics(host, path):
    file_content = DEFAULTS.get_file_data(path)
    content_type = DEFAULTS.get_file_type(path)
    response = DEFAULTS.generate_response(200,
                                          server=host,
                                          file_content=file_content,
                                          content_type=content_type)
    return response
