from backend import render


def main(request, params):
    args = {
        'var_1': ''
    }
    if not params == {}:
        args = {
            'var_1': params['user-input']
        }
    return render.render(request, 'files/index.html', args)


if __name__ == '__main__':
    test = main({'method': 'GET', 'path': '/index', 'query_params': {'user-input': 'test'}, 'headers': {'Host': '192.168.115.200', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Referer': 'http://192.168.115.200/index', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'Cookie': 'csrftoken=B1odSJXf4eboWL6Su1lumC8FV61BHjOs'}, 'body': ''})
    print(test)
