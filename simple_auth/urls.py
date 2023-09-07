from django.urls import path

from .views import register, login_request, logout_request

app_name = "simple_auth"

urlpatterns = [
    path("creer_compte", register, name="register"),
    path("identification", login_request, name="login"),
    path("deconnexion", logout_request, name="logout"),
]
