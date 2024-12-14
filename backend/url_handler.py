from backend import DEFAULTS, router
import logging
import os.path
import urls


def handle(request):
    return router.Router(urls.URL_PATTERNS).resolve(request['path'], request)


def get_statics(request):
    file_path = os.path.join(DEFAULTS.STATIC, request['path'].lstrip('/'))
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

