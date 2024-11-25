from backend import render, request_handler


def main(request):
    args = {
        'var_1': '',
        'var_2': '',
        'var_3': 'Welcome!',
        'info': ''
    }

    if request['method'] == 'POST':
        params = request_handler.get(request['body'])
        args = {
            'var_1': params['username'],
            'var_2': params['password']
        }
        if args['var_1'] == 'robert' and args['var_2'] == '1234':
            args['var_3'] = 'Success!'
            args['info'] = 'Your login was successful!'
        else:
            args['var_3'] = 'Welcome!'
            args['info'] = 'Wrong credentials! Try username <b>robert</b> and password <b>1234</b>'
    return render.render(request, 'files/index.html', args)

