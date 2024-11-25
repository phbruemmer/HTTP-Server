import urls


def check_urls(url):
    valid = False
    if url in urls.URL_PATTERNS:
       valid = True
    return valid


def handle(request):
    response = urls.URL_PATTERNS[request['path']](request)
    return response
