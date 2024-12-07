import DEFAULTS


def render(request, path, args=None, **kwargs):
    host = kwargs.get('host')

    file_data = ''
    with open(path, 'r') as file:
        file_data += file.read()

    if args:
        for argument in args:
            target = "{{ " + argument + " }}"
            if len(args[argument]):
                file_data = file_data.replace(target, args[argument])
            else:
                file_data = file_data.replace(target, '')
    content_type = DEFAULTS.get_file_type(path)

    return DEFAULTS.generate_response(200, server=host, file_content=file_data.encode(), content_type=content_type)


if __name__ == '__main__':
    args_ = {
        'var_1': 'Test 1',
        'var_2': 'Test 2'
    }
    print(render('Hans', 'C:\\Users\\phbru\\PycharmProjects\\HTTP-Server\\files\\index.html', args_))
