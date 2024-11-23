import views

URL_PATTERNS = {
    '/index': views.main,
}


if __name__ == "__main__":
    var = URL_PATTERNS['/index']('nothing')
    print(var)
