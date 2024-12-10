import urls


def check_urls(url):
    if url in urls.URL_PATTERNS:
        return True
    return False


def handle(request):
    response = urls.URL_PATTERNS[request['path']](request)
    return response
