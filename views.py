import DEFAULTS


def main(request):
    return DEFAULTS.generate_response(200, '0.0.0.0', 'C:\\Users\\phbru\\PycharmProjects\\HTTP-Server\\files\\index.html', True)
