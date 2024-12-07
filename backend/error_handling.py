from backend import render
import settings

DEFAULT_MESSAGES = {
    404: {'title': '404 - Not Found', 'info': 'The requested URL was not found.'},
    500: {'title': '500 - Internal Server Error', 'info': 'Unexpected error. Please contact no one and leave me alone.'},
}


def render_error(host, code):
    path = settings.DEFAULT_PATHS['error_template']
    return render.render(request=None, path=path, args=DEFAULT_MESSAGES[code], host=host)
