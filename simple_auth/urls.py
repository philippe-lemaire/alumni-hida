from django.urls import path

from .views import (
    login_request,
    logout_request,
    PasswordChangeView,
    password_reset_view,
)

app_name = "simple_auth"

urlpatterns = [
    path("identification", login_request, name="login"),
    path("deconnexion", logout_request, name="logout"),
    path("modifier-mot-de-passe", PasswordChangeView.as_view(), name="update_password"),
    path(
        "réinitialiser-le-mot-de-passe",
        password_reset_view,
        name="reset_password",
    ),
]
