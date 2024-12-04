import DEFAULTS


def redirect(old_path, url):
    return DEFAULTS.generate_response(302, '0.0.0.0', old_path, True, location=url)


# generate_response(302, "MyServer", "/old-path", close_connection=False, location="/new-path")
