from django.contrib.auth.forms import AuthenticationForm
from django import forms


class AuthenticationUserForm(AuthenticationForm, forms.Form):

    username = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'class': 'input', 'type': 'text', 'placeholder': "Username", }))
    password = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'class': 'input', 'type': 'text', 'placeholder': "Password", }))