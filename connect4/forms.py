from .models import *
from django import forms
from django.forms import ModelForm

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ("username",
                      "password")

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = auth.authenticate(username=username,
                                 password=password)
        return user

class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ("username",
                      "email",
                      "password")

        labels = {
            "username": "Username",
            "email": "Email",
            "password":"Password",
        }

        widgets = {
            "password": forms.PasswordInput(),
        }

    def clean_email(self):
        # ensure that the email address supplied is unique
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email)
        if exists:
            self.add_error("password", "This email already exists")
        return email

    def create_user(self, *args, **kwargs):
        # take the validated data and sign the user up.
        data = self.cleaned_data
        user = User.objects.create_user(data["username"], data["email"], data["password"])
        return user
