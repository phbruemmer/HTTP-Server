from backend import DEFAULTS
import re
import os.path
import settings


def render(request, path, args=None, **kwargs):
    """
    renders the file (from path parameter) and changes given arguments to the given value (including template code)
    :param request: string (HTTP request)
    :param path: string (file path)
    :param args: dictionary (variable_name : value)
    :param kwargs:
    :return:
    """
    host = kwargs.get('host')

    file_data = ''

    with open(path, 'r') as file:
        file_data += file.read()

    file_data = find_template_code(file_data)

    if args:
        for argument in args:
            target = "{{ " + argument + " }}"
            if len(args[argument]):
                file_data = file_data.replace(target, args[argument])
            else:
                file_data = file_data.replace(target, '')
    content_type = DEFAULTS.get_file_type(path)

    return DEFAULTS.generate_response(200, server=host, file_content=file_data.encode(), content_type=content_type)


def methods(method, content):
    """
    Handles the different methods in the HTML
    :param method: string
    :param content: value from the template code
    :return: processed value
    """
    value = ''

    match method:
        case 'static':
            value = os.path.join(settings.DEFAULT_STATIC_FILE_PATH, content)
    return value


def find_template_code(document):
    """
    Finds template code in the HTML and overwrites it with new values. (e.g. {% static 'file/path.css' %})
    :param document: file content
    :return: new document content
    """
    parts = re.findall(r"{%.*?%}", document)
    for part in parts:
        separator = part.split(' ')
        new_part = methods(separator[1], separator[2])
        document = document.replace(part, new_part)
    return document
