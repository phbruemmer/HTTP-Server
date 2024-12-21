from backend import request_handler
from backend.cookie_handling import cookies
from backend.responses import render, redirect
from backend.database import database_connector as dc
from loginApp.modules import session_id
import hashlib


def main(request):
    args = {
        'var_3': 'Welcome!',
        'info': ''
    }

    if request.get("method") == 'POST':
        params = request_handler.get(request['body'])
        user_id = dc.get_id('users', 'username', params['username'], force_clean=True)
        hash_object = hashlib.sha256()
        hash_object.update(params['password'].encode())
        hash_hex = hash_object.hexdigest()
        if user_id and dc.get_by_id('users', user_id)[3] == hash_hex:
            session_value, session_hex = session_id.create()
            session_cookie = cookies.create('HttpOnly', path="/", session_id=session_value)
            # Updates the session_id column in the users table of the database
            dc.update_column('users', 'session_id', session_hex, 'id', user_id)
            return redirect.redirect('/', cookies=[session_cookie])
            # return render.render(request, 'HTML_files/home.html', args)
        else:
            args['var_3'] = 'Welcome!'
            args['info'] = '<b>Wrong credentials!</b>'
    return render.render(request, 'loginApp/HTML_files/index.html', args)


def register(request):
    args = {
        'var_3': 'Welcome!',
        'info': ''
    }

    if request.get("method") == 'POST':
        params = request_handler.get(request['body'])
        if not params['password-0'] == params['password-1']:
            args['info'] = 'Password does not match!'
        else:
            hash_object = hashlib.sha256()
            hash_object.update(params['password-0'].encode())
            hash_hex = hash_object.hexdigest()

            if not all(dc.validate('users', params[field], column_name=field) for field in ['username', 'email']):
                user_data = {
                    'username': params["username"],
                    'email': params["email"],
                    'password': hash_hex
                }
                dc.write('users', user_data)
                return redirect.redirect('/')
            else:
                args['info'] = 'Account already exists.'
    return render.render(request, 'loginApp/HTML_files/register.html', args)
