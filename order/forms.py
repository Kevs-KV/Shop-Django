from order.models import Order
from django import forms

class OrderForm(forms.ModelForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'input', 'type': 'text', 'name': 'first_name', 'placeholder': "First Name"}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'input', 'type': 'text', 'name': 'last_name', 'placeholder': "Last Name"}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class': 'input', 'type': 'text', 'name': 'email', 'placeholder': "Email"}))
    address = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'input', 'type': 'text', 'name': 'address', 'placeholder': "Address"}))
    city = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'input', 'type': 'text', 'name': 'city', 'placeholder': "City"}))
    country = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'input', 'type': 'text', 'name': 'country', 'placeholder': "Country"}))
    telephone = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'input', 'type': 'tel', 'name': 'tel', 'placeholder': "Telephone"}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'city', 'country', 'telephone']