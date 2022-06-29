from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm, UserCreationForm,
)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .tasks import send_email_password_reset


class SignupForm(UserCreationForm):
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    username = forms.CharField(label=_("Username"),
                               widget=forms.TextInput(
                                   attrs={'class': 'input', 'type': 'text', 'placeholder': "Username", }))
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'input', 'type': 'text', 'placeholder': "Password", "autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'input', 'type': 'text', 'placeholder': "Password", "autocomplete": "new-password", }),
        strip=False,
    )
    email = forms.EmailField(widget=forms.TextInput(
                                attrs={'class': 'input', 'type': 'email', 'placeholder': "Email",}), max_length=200, help_text='Required')

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
