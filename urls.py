from backend.router import path, include
from loginApp import urls as login_urls
import views

URL_PATTERNS = [
    path('/', views.home),
    path('/account', include(login_urls))
]
