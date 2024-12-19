def create(*args, **kwargs):
    """
    creates a cookie header for the HTTP response.
    :return: string (cookie header)
    """
    kwargs.get("expires", "")
    kwargs.get("max_age", "")

    cookie = "Set-Cookie: "

    # Add key-value pairs from kwargs
    for param in kwargs:
        cookie += f"{param}={kwargs[param]}; "

    # Add security flags
    for arg in args:
        cookie += f"{arg}; "
    return cookie + "\r\n"


if __name__ == '__main__':
    header = create(expires="Wed, 19 Jan 2038 03:14:07 GMT", max_age=3600, user_id="12345", session_id="abcde")
    print(header)
