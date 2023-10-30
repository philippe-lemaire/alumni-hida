from django.shortcuts import render, redirect
from .forms import PasswordResetForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from trombinoscope.models import CustomUser
from django.urls import reverse
from templated_email import send_templated_mail
from django.http import HttpResponseRedirect
from django.conf import settings


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


def password_reset_view(request):
    template_name = "simple_auth/reset-password.html"
    form = PasswordResetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            # check if there is a user with this email
            email = form.cleaned_data["email"]
            try:
                user = CustomUser.objects.get(email=email)
                print(user)
                uri = request.build_absolute_uri(
                    reverse(
                        "trombinoscope:set_password",
                        args=(str(user.id),),
                    )
                )
                # send mail with templated-email
                send_templated_mail(
                    template_name="reset_password_mail",
                    from_email=settings.EMAIL_FROM,
                    recipient_list=[email],
                    context={"uri": uri},
                )

                messages.success(request, "Email envoyé")
                return HttpResponseRedirect("/")

            # if not, write a message and redirect to this same url in get
            except CustomUser.DoesNotExist:
                messages.warning(request, "Aucun compte enregistré avec cet email.")

    context = {"form": form}
    return render(request, template_name, context)


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "simple_auth/password_reset_confirm.html"
    post_reset_login = True
    success_url = "/"
