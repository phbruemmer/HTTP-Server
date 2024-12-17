from backend import DEFAULTS
import re
import os.path
import settings


def render(request, path, args=None, **kwargs):
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
    value = ''

    match method:
        case 'static':
            value = os.path.join(settings.DEFAULT_STATIC_FILE_PATH, content)
    return value


def find_template_code(document):
    parts = re.findall(r"{%.*?%}", document)
    for part in parts:
        separator = part.split(' ')
        new_part = methods(separator[1], separator[2])
        document = document.replace(part, new_part)
    return document
