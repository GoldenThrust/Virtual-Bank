from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.IntegerField(required=True)
    date_of_birth = forms.DateInput()
    profile_picture = forms.ImageField(required=True)
    address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    country = forms.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "profile_picture",
            "email",
            "password1",
            "password2",
            "address",
            "city",
            "state",
            "country",
            "date_of_birth",
        ]
