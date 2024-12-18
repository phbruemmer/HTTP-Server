from backend.router import path, include
from loginApp import urls as login_urls
from main import urls as main_urls

URL_PATTERNS = [
    path('/', include(main_urls)),
    path('/account', include(login_urls))
]
