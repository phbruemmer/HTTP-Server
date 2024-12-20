from backend.router import path
from loginApp import views


URL_PATTERNS = [
    path('/login', views.main),
    path('/register', views.register),
]
