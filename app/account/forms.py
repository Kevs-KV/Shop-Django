from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm, UserCreationForm,
)
from django.contrib.auth.models import User

from .tasks import send_email_password_reset


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AuthenticationUserForm(AuthenticationForm, forms.Form):
    username = forms.CharField(label='',
                               widget=forms.TextInput(
                                   attrs={'class': 'input', 'type': 'text', 'placeholder': "Username", }))
    password = forms.CharField(label='',
                               widget=forms.TextInput(
                                   attrs={'class': 'input', 'type': 'text', 'placeholder': "Password", }))


class CreateUserForm(forms.Form):
    username = forms.CharField(label='',
                               widget=forms.TextInput(
                                   attrs={'class': 'input', 'type': 'text', 'placeholder': "Username", }))

    email = forms.CharField(label='',
                            widget=forms.TextInput(
                                attrs={'class': 'input', 'type': 'email', 'placeholder': "Email", }))

    password = forms.CharField(label='',
                               widget=forms.TextInput(
                                   attrs={'class': 'input', 'type': 'text', 'placeholder': "Password", }))


class UserPasswordResetForm(PasswordResetForm):

    def send_mail(self, subject_template_name, email_template_name, context,
                  from_email, to_email, html_email_template_name=None):
        context['user'] = context['user'].id

        send_email_password_reset.delay(subject_template_name=subject_template_name,
                                        email_template_name=email_template_name,
                                        context=context, from_email=from_email, to_email=to_email,
                                        html_email_template_name=html_email_template_name)
