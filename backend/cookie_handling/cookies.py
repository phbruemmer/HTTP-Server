import logging


def create(*args, **kwargs):
    """
    Creates a Set-Cookie header for the HTTP response (without the 'Set-Cookie:' field prefix)
    :return: string (cookie header)
    """
    cookie = "Set-Cookie: "

    # Add other key-value pairs from kwargs (e.g., user_id, session_id)
    for param, value in kwargs.items():
        if param not in ['expires', 'max_age', 'path']:
            cookie += f"{param}={value}; "

    # Add security flags (from *args)
    for arg in args:
        cookie += f"{arg}; "

    path = kwargs.get('path', '/')
    cookie += f"path={path}; "

    if 'expires' in kwargs:
        cookie += f"expires={kwargs['expires']}; "
    if 'max_age' in kwargs:
        cookie += f"max-age={kwargs['max_age']}; "

    cookie = cookie.strip('; ')

    logging.info("[cookie - create] Created new cookie.")

    return cookie


if __name__ == '__main__':
    header = create(max_age=3600, user_id="12345", session_id="abcde")
    print(header)
