from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import NewAlumniForm


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
            emails = emails.split()
            counter = 0
            for email in emails:
                # check if user with email already exists, write messages.warning(request, "utilisateur déjà inscrit") if True
                # send email invite
                counter += 1
            messages.success(request, f"{counter} anciens élèves invités")

        return HttpResponseRedirect("/")
    else:  # it's a get method
        context = {"form": NewAlumniForm()}
        return render(request, "trombinoscope/invite_users.html", context=context)
