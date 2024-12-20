from backend.router import path
from main import views

URL_PATTERNS = [
    path('', views.home),
]
