from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.urls import reverse

from .forms import NewAlumniForm, UpdateProfileForm
from .models import CustomUser


class IndexView(TemplateView):
    template_name = "trombinoscope/index.html"


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
                    user = CustomUser(email=email, password=password)
                    # save user
                    user.save()

                    uri = request.build_absolute_uri(
                        reverse(
                            "trombinoscope:update_profile",
                            args=(str(user.id),),
                        )
                    )
                    # send mail to user
                    send_mail(
                        subject="Vous avez été invité·e à rejoindre le trombinoscope des anciens élèves HIDA du Lycée Public de Saint-Just",
                        message=f"Bonjour. Un·e enseignant·e HIDA vous a invité à rejoindre le trombinoscope des anciens élèves. Voici le lien pour confirmer votre compte et compléter votre profil {uri}. It should contain a link to the site, that is unique. Your password is {password}. ",
                        from_email="from@example.com",
                        recipient_list=[email],
                        fail_silently=False,
                    )

                    counter += 1
            messages.success(request, f"{counter} anciens élèves invités")

        return HttpResponseRedirect("/")
    else:  # it's a get method
        context = {"form": NewAlumniForm()}
        return render(request, "trombinoscope/invite_users.html", context=context)


def update_profile_view(request, id):
    user = CustomUser.objects.get(id=id)
    if request.method == "POST":
        # verify the form and update user, then redirect to home page
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.confirmed_account = True
            user.save()
            messages.success(request, message="Profil mis à jour.")
            return HttpResponseRedirect("/")
    else:
        # instanciate the form and render the template

        form = UpdateProfileForm(instance=user)
        return render(
            request, "trombinoscope/update_profile.html", {"form": form, "id": id}
        )
