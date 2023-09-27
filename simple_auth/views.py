from django.shortcuts import render, redirect
from .forms import PasswordResetForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from trombinoscope.models import CustomUser
from django.urls import reverse
from django.core.mail import send_mail
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
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # check if there is a user with this email
            email = form.cleaned_data["email"]
            try:
                user = CustomUser.objects.get(email=email)

                uri = request.build_absolute_uri(
                    reverse(
                        "trombinoscope:set_password",
                        args=(str(user.id),),
                    )
                )
                # send mail to user
                send_mail(
                    subject="Réinitialisation de mot de passe sur le trombinoscope des élèves HIDA du Lycée Public de Saint-Just",
                    message=f"Vous avez demandé à réinitialiser votre mot de passe sur le trombinoscope des élèves HIDA du Lycée Public de Saint-Just.\nVoici le lien pour modifier votre mot de passe {uri}. ",
                    from_email="from@example.com",
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, "Email envoyé")
                return HttpResponseRedirect("/")

            # if not, write a message and redirect to this same url in get
            except:
                messages.warning(request, "Aucun compte enregistré avec cet email.")
                return render(request, template_name, {"form": form})
    else:
        form = PasswordResetForm()
        context = {"form": form}
        return render(request, template_name, context)


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "simple_auth/password_reset_confirm.html"
    post_reset_login = True
    success_url = "/"
