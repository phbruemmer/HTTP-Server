from backend import error_handling
import logging


class Route:
    def __init__(self, pattern, view, name=None):
        self.pattern = pattern
        self.view = view
        self.name = name


class Router:
    def __init__(self, routes):
        self.routes = routes

    def resolve(self, pattern, request=None):
        logging.info("[resolve] Trying to resolve %s", pattern)
        for route in self.routes:
            if route.pattern == pattern:
                logging.info("[resolve] Pattern found - Executing view function...")
                return route.view(request)
        logging.info("[GET] No such path found - 404 Not Found.")
        return error_handling.render_error(None, 404)


def path(pattern, view, name=None):
    """
    This function returns a Route object for a single path.
    :param pattern: resource URL
    :param view: the view function you want to execute when accessing this URL
    :param name: name of the path
    :return: Route Object with pattern, view, name
    """
    return Route(pattern, view, name)


def include(paths):
    """
    This function returns the paths of other urls.py files
    :param paths:
    :return:
    """
    pass

