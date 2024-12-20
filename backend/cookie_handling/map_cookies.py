def parse(cookie_header):
    if cookie_header is not None:
        single_cookies = cookie_header.split('; ')
        cookie_map = {}

        for cookie in single_cookies:
            cookie, value = cookie.split('=')
            cookie_map[cookie] = value
        return cookie_map
