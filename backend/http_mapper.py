import logging


def map_request(request):
    """
    Converts HTTP request to hashmap for better processing.
    :param request: HTTP request (string)
    :return: request hashmap / dictionary
    """
    try:
        lines = request.split("\r\n")
        method, path_with_query, version = lines[0].split(" ")
    except ValueError as e:
        logging.error("[map_request] Malformed request: %s", e)
        raise ValueError("Invalid HTTP request line.")

    query_params = {}

    if '?' in path_with_query:
        path, query_string = path_with_query.split('?', 1)
        for param in query_string.split('&'):
            arg = param.split('=')
            query_params[arg[0]] = arg[1]
    else:
        path = path_with_query

    headers = {}
    for line in lines[1:]:
        if line == "":
            break
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()

    body_index = lines.index("") + 1 if "" in lines else len(lines)
    body = "\n".join(lines[body_index:])

    return {
        "method": method,
        "path": path,
        "query_params": query_params,
        "headers": headers,
        "body": body,
    }
