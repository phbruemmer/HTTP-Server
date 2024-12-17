from backend import url_handler, error_handling
import logging


def GET(HOST, request):
    """
    Handles GET method from the HTTP request.
    :param HOST: Host
    :param request: request Hashmap with HTTP information
    :return:
    """

    if 'html' in request['headers']['Accept']:
        logging.info("[GET] Path found - 200 OK")
        response = url_handler.handle(request)
    elif 'css' in request['headers']['Accept']:
        logging.info("[GET] adding css - 200 OK")
        path = url_handler.get_statics(request)  # For safe file handling
        if path is not None:
            response = url_handler.handle_statics(HOST, path)
        else:
            response = error_handling.render_error(HOST, 404)
    else:
        logging.info("[GET] No such path found - 404 Not Found.")
        response = error_handling.render_error(HOST, 404)
    return response
