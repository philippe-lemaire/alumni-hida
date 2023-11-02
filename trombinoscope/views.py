from django.views.generic import TemplateView, ListView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from templated_email import send_templated_mail
from django.urls import reverse
from django.contrib.auth import login
from django.conf import settings
from django.db.models import Q
from django.core.mail import EmailMessage


from .forms import (
    NewAlumniForm,
    UpdateProfileForm,
    PasswordSetForm,
    SearchForm,
    ContactForm,
)
from .models import CustomUser


class IndexView(TemplateView):
    template_name = "trombinoscope/index.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET or None)
        return context


def contact_view(request):
    template_name = "trombinoscope/contact.html"
    search_form = SearchForm(request.GET or None)
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            form_user_email = contact_form.cleaned_data["email"]
            message = contact_form.cleaned_data["message"]
            email = EmailMessage(
                subject="Formulaire de contact du site annuaire HIDA",
                body=f"De : {form_user_email}\n\n{message}",
                from_email=settings.EMAIL_FROM,
                to=[settings.CONTACT_EMAIL],
                reply_to=[form_user_email],
            )
            email.send()
            messages.success(request, "Votre message a été envoyé.")
            return HttpResponseRedirect("/")
    else:
        context = {"search_form": search_form, "contact_form": ContactForm()}
        return render(request, template_name, context)


@staff_member_required
def invite_users_view(request):
    if request.method == "POST":
        # validate the form and do stuff with it
        form = NewAlumniForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL
            emails = form.cleaned_data["emails"]
            # turn emails into a real list of emails
            emails = emails.replace(",", " ").replace(";", " ").replace("\t", " ")
            emails = emails.split()
            counter = 0
            # Query the confirmed users
            non_confirmed_users = CustomUser.objects.filter(confirmed_account=False)
            confirmed_users = CustomUser.objects.filter(confirmed_account=True)
            staff_users = CustomUser.objects.filter(is_staff=True)
            for email in emails:
                # check if user with email already exists, write messages.warning(request, "utilisateur déjà inscrit") if True
                if confirmed_users.filter(email=email):
                    messages.warning(
                        request,
                        message=f"L’utilisateur ayant l’email {email} est déjà inscrit.",
                    )
                    return HttpResponseRedirect("/")
                elif staff_users.filter(email=email):
                    messages.warning(
                        request,
                        message=f"L’utilisateur ayant l’email {email} fait partie de l’équipe du site.",
                    )

                # send email invite
                else:
                    # check if unconfirmed account exists : if true, delete the user before recreating it
                    if non_confirmed_users.filter(email=email):
                        user = CustomUser.objects.get(email=email)
                        user.delete()
                        print("user_deleted")
                        messages.warning(
                            request,
                            message=f"L’utilisateur ayant l’email {email} avait déjà été invité mais n’avait pas confirmé son compte, une nouvelle invitation lui est adressée.",
                        )
                    # create user
                    password = "changeme"
                    user = CustomUser.objects.create_user(email, password)

                    # save user
                    user.save()

                    uri = request.build_absolute_uri(
                        reverse(
                            "trombinoscope:set_password",
                            args=(str(user.id),),
                        )
                    )
                    # send mail with templated email

                    send_templated_mail(
                        template_name="welcome",
                        from_email=settings.EMAIL_FROM,
                        recipient_list=[email],
                        context={"uri": uri},
                    )

                    counter += 1
            messages.success(request, f"{counter} anciens élèves invités")

        return HttpResponseRedirect("/")
    else:  # it's a get method
        context = {"form": NewAlumniForm()}
        return render(request, "trombinoscope/invite_users.html", context=context)


def password_set_view(request, id):
    user = CustomUser.objects.get(id=id)
    if request.method == "POST":
        form = PasswordSetForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]

            user.set_password(password)
            user.confirmed_account = True
            user.save()
            messages.success(request, "Mot de passe enregistré.")
            login(request, user)
            messages.success(
                request, "Vous êtes identifié·e. Pensez à compléter votre profil."
            )
            return HttpResponseRedirect(reverse("trombinoscope:update_profile"))
    else:
        form = PasswordSetForm()
        return render(
            request, "trombinoscope/set_password.html", context={"form": form, "id": id}
        )


def update_profile_view(request):
    user = request.user
    form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=user)

    if request.method == "POST":
        # verify the form and update user, then redirect to home page
        if form.is_valid():
            user.confirmed_account = True
            form.save()
            messages.success(request, message="Profil mis à jour.")

            redirect_uri = request.build_absolute_uri(
                reverse("trombinoscope:update_profile")
            )
            return HttpResponseRedirect(redirect_uri)
    return render(
        request,
        "trombinoscope/update_profile.html",
        {"form": form, "user": user},
    )


def pre_delete_profile_view(request):
    template_name = "trombinoscope/pre_delete_profile.html"
    context = {}
    return render(request, template_name, context)


def delete_profile_view(request):
    user = request.user
    user.delete()
    messages.success(request, message="Votre profil a été supprimé.")
    return HttpResponseRedirect("/")


class AlumniList(LoginRequiredMixin, ListView):
    paginate_by = 6
    context_object_name = "alumni"
    queryset = CustomUser.objects.filter(confirmed_account=True, is_staff=False)
    template_name = "trombinoscope/alumni_list.html"
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET or None)
        return context


@login_required
def alumni_search_result(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            term = form.cleaned_data["search_term"]

            queryset = CustomUser.objects.filter(
                confirmed_account=True, is_staff=False
            ).filter(
                Q(post_bac__contains=term)
                | Q(occupation__contains=term)
                | Q(first_name__contains=term)
                | Q(last_name__contains=term)
            )

            context = {"alumni": queryset, "search_form": form}
            template_name = "trombinoscope/alumni_list.html"
            return render(request, template_name, context)
    else:
        return HttpResponseRedirect("/")


@staff_member_required
def staff_edit_profile(request, id):
    user = CustomUser.objects.get(id=id)

    if request.method == "POST":
        # verify the form and update user, then redirect to home page
        form = UpdateProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user.confirmed_account = True
            form.save()
            messages.success(request, message="Profil mis à jour.")
            redirect_uri = request.build_absolute_uri(
                reverse("trombinoscope:alumni_list")
            )
            return HttpResponseRedirect(redirect_uri)
    else:
        # instanciate the form and render the template
        form = UpdateProfileForm(instance=user)
        return render(
            request,
            "trombinoscope/staff_update_profile.html",
            {"form": form, "id": id},
        )
