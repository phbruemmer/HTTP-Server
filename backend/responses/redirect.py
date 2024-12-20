from backend import DEFAULTS


def redirect(url, **kwargs):
    cookie_header = kwargs.get("cookies", "")
    return DEFAULTS.generate_response(302, location=url, cookies=cookie_header)


# generate_response(302, "MyServer", "/old-path", close_connection=False, location="/new-path")
