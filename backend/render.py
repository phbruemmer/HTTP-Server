import DEFAULTS


def render(request, path, args=None):
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

    return DEFAULTS.generate_response(200, '0.0.0.0', path, True, modified_file=file_data)


if __name__ == '__main__':
    args_ = {
        'var_1': 'Test 1',
        'var_2': 'Test 2'
    }
    print(render('Hans', 'C:\\Users\\phbru\\PycharmProjects\\HTTP-Server\\files\\index.html', args_))
