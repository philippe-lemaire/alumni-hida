from django.urls import path

from .views import (
    login_request,
    logout_request,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)

app_name = "simple_auth"

urlpatterns = [
    path("identification", login_request, name="login"),
    path("deconnexion", logout_request, name="logout"),
    path("modifier-mot-de-passe", PasswordChangeView.as_view(), name="update_password"),
    path(
        "réinitialiser-le-mot-de-passe",
        PasswordResetView.as_view(),
        name="reset_password",
    ),
    path(
        "réinitialiser-le-mot-de-passe-confirmation",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
