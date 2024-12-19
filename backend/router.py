from backend.responses import error_handling
import logging


class Route:
    """
    Route class to create single route objects for URL patterns
    """
    def __init__(self, pattern, view, name=None):
        self.pattern = pattern
        self.view = view
        self.name = name


class Router:
    def __init__(self, routes):
        self.routes = self.flatten_routes(routes)

    def flatten_routes(self, routes, prefix=""):
        """
        Flattens the routes to include paths from different apps.
        :param routes: URL_PATTERNS List
        :param prefix: needed for recursive function calls (keep default)
        :return:
        """
        logging.info("[flatten_routes] flattening routes...")
        flat_routes = []
        for route in routes:
            if isinstance(route.view, list):
                prefixed_routes = self.flatten_routes(route.view, prefix + route.pattern)
                flat_routes.extend(prefixed_routes)
            else:
                flat_routes.append(Route(prefix + route.pattern, route.view, route.name))
        logging.info("[flatten_routes] routes flattened.")
        return flat_routes

    def resolve(self, pattern, request=None):
        """
        Tries to find a pattern (pattern parameter) in the flattened URL vector.
        :param pattern: string
        :param request: string (default None)
        :return:
        """
        logging.info("[resolve] Trying to resolve %s", pattern)
        for route in self.routes:
            if route.pattern == pattern:
                logging.info("[resolve] Pattern found - Executing view function...")
                return route.view(request)
        logging.info("[GET] No such path found - 404 Not Found.")
        return error_handling.render_error(None, 404)


def path(pattern, view, name=None):
    """
    This function returns a Route object for a single path to a specific view.
    :param pattern: resource URL
    :param view: the view function you want to execute when accessing this URL
    :param name: name of the path
    :return: Route Object with pattern, view, name
    """
    return Route(pattern, view, name)


def include(app):
    """
    This function returns the paths of other urls.py files
    :param app: path reference
    :return:
    """
    return app.URL_PATTERNS
