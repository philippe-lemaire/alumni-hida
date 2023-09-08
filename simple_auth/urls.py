from django.urls import path

from .views import login_request, logout_request

app_name = "simple_auth"

urlpatterns = [
    path("identification", login_request, name="login"),
    path("deconnexion", logout_request, name="logout"),
]
