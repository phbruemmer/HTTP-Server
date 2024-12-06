import DEFAULTS


def redirect(url):
    return DEFAULTS.generate_response(302, location=url)


# generate_response(302, "MyServer", "/old-path", close_connection=False, location="/new-path")
