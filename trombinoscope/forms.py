from django import forms


class NewAlumniForm(forms.Form):
    emails = forms.CharField(
        label="Emails des étudiants à inviter :",
        max_length=2000,
        widget=forms.TextInput(attrs={"placeholder": "kikidu69@skyrock.com"}),
    )
