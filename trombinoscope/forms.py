from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from captcha.fields import CaptchaField
from tinymce.widgets import TinyMCE


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
            "email",
            "first_name",
            "last_name",
            "photo",
            "bac_year",
            "status",
            "post_bac",
            "occupation",
            "contact_info_instagram",
            "contact_info_email",
            "contact_info_linkedin",
            "contact_info_tel",
        ]
        widgets = {"content": TinyMCE(attrs={"cols": 80, "rows": 30})}


class PasswordSetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


class SearchForm(forms.Form):
    search_term = forms.CharField(
        label="",
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "Une école, un nom…"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-inline"
        self.helper.form_action = "trombinoscope:search"
        self.helper.layout = Layout(
            "search_term",
        )
        self.helper.add_input(
            Submit(
                "submit",
                "Chercher",
                css_class="m-1 btn-secondary",
            )
        )


class ContactForm(forms.Form):
    email = forms.EmailField(label="Votre email :", max_length=200)
    message = forms.CharField(
        label="Votre message :", max_length=200, widget=forms.Textarea()
    )
    captcha = CaptchaField()
