import views

URL_PATTERNS = {
    '/login': views.main,
    '/register': views.register,
    '/home': views.home,
}


if __name__ == "__main__":
    var = URL_PATTERNS['/index']('nothing')
    print(var)
