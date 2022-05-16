from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User


class AuthenticationUserForm(AuthenticationForm, forms.Form):

    username = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'class': 'input', 'type': 'text', 'placeholder': "Username", }))
    password = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'class': 'input', 'type': 'text', 'placeholder': "Password", }))

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