def get(data):
    body_map = {}

    if '&' in data and data is not None:
        for arg in data.split('&'):
            b_arg = arg.split('=')
            body_map[b_arg[0]] = b_arg[1]
    else:
        if data is not None:
            b_arg = data.split('=')
            body_map[b_arg[0]] = b_arg[1]
    return body_map

