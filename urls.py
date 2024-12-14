from backend.router import path, include
import views

URL_PATTERNS = [
    path('/login', views.main),
    path('/register', views.register),
    path('/', views.home)
]
