
"""

 Set-Cookie: letzteSuche=Y29va2llIGF1ZmJhdQ==;
             expires=Tue, 29-Mar-2014 19:30:42 GMT;
             Max-Age=2592000;
             Path=/cgi/suche.py

"""


def create(expires, max_age, **kwargs):
    cookie = "Set-Cookie: "
    for param in kwargs:
        cookie += param + '=' + kwargs[param] + ';\r\n'
    cookie += f'expires={expires};\r\nMax-Age={max_age};\r\nSecure; HttpOnly;\r\n'
    return cookie


if __name__ == '__main__':
    data = create('Tue, 29-Mar-2014 19:30:42 GMT', 2592000, letzteSuche='Y29va2llIGF1ZmJhdQ==')
    print(data)
