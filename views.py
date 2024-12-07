from backend import render, request_handler, redirect, database_connector as dc
import hashlib


def main(request):
    args = {
        'var_3': 'Welcome!',
        'info': ''
    }

    if request['method'] == 'POST':
        params = request_handler.get(request['body'])
        user_id = dc.get_id('users', 'username', params['username'], force_clean=True)
        hash_object = hashlib.sha256()
        hash_object.update(params['password'].encode())
        hash_hex = hash_object.hexdigest()
        if user_id and dc.get_by_id('users', user_id)[3] == hash_hex:
            return redirect.redirect('/home')
            # return render.render(request, 'files/home.html', args)
        else:
            args['var_3'] = 'Welcome!'
            args['info'] = '<b>Wrong credentials!</b>'
    return render.render(request, 'files/index.html', args)


def register(request):
    args = {
        'var_3': 'Welcome!',
        'info': ''
    }

    if request['method'] == 'POST':
        params = request_handler.get(request['body'])
        if not params['password-0'] == params['password-1']:
            args['info'] = 'Password does not match!'
        else:
            hash_object = hashlib.sha256()
            hash_object.update(params['password-0'].encode())
            hash_hex = hash_object.hexdigest()

            if dc.validate('users', params['username'], 1) and dc.validate('users', params['email'], 2):
                dc.write('users', (params['username'], params['email'], hash_hex))
                return redirect.redirect('/home')
            else:
                args['info'] = 'Account already exists.'

    return render.render(request, 'files/register.html', args)


def home(request):
    args = {
        'username': 'test',
    }
    return render.render(request, 'files/home.html', args)
