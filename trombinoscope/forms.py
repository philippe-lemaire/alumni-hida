from django import forms
from django.forms import ModelForm
from .models import CustomUser


class NewAlumniForm(forms.Form):
    emails = forms.CharField(
        label="Emails des étudiants à inviter :",
        max_length=2000,
        widget=forms.TextInput(
            attrs={"placeholder": "kikidu69@skyrock.com, lola@kikoo.com"}
        ),
    )


class UpdateProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "photo",
            "bac_year",
            "status",
            "looking_for_internship",
            "enseignant_hida",
            "contact_info_instagram",
            "contact_info_email",
            "contact_info_linkedin",
            "contact_info_tel",
        ]
