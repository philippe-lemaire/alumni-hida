from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Bienvenue, {user.first_name}.")
                return redirect("/")
            else:
                messages.error(request, "Email ou mot de passe invalide.")
        else:
            messages.error(request, "Email ou mot de passe invalide.")
    form = AuthenticationForm()
    return render(
        request=request,
        template_name="simple_auth/login.html",
        context={"login_form": form},
    )


def logout_request(request):
    logout(request)
    messages.info(request, "Vous êtes déconnecté·e.")
    return redirect("/")


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = "simple_auth/change-password.html"
    success_url = "/"


class PasswordResetView(auth_views.PasswordResetView):
    template_name = "simple_auth/reset-password.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "simple_auth/password_reset_confirm.html"
    post_reset_login = True
    success_url = "/"
