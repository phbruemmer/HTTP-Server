from backend.responses import render, redirect
from backend.cookie_handling import map_cookies
from backend.database import database_connector as dc


def home(request):
    """
    The start page is only accessible if a valid session ID cookie is present.
    """
    cookies = request.get('headers').get('Cookie')
    cookies = map_cookies.parse(cookies)

    # print(cookies)

    if cookies is None:
        print("[home] No cookies")
        return redirect.redirect('/account/login')

    user_id = dc.get_id('users', 'session_id', cookies.get('session_id'), force_clean=True)
    # print(user_id)

    if user_id is None:
        print("[home] No valid session id found")
        return redirect.redirect('/account/login')

    args = {
        'username': dc.get_column_value_by_id('users', user_id, 'username'),
    }

    return render.render(request, 'main/HTML_files/home.html', args)
