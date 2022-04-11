from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML
from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'type': 'text', 'placeholder': "Your Name"}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'type': 'email', 'placeholder': "Your Email"}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'input', 'placeholder': "Your Review"}))
    star = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'name': 'rating', 'id': 'star' }))
    # star1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'name': 'rating', 'type': 'radio', 'id': 'star1', 'value': 1, }))
    # star2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'name': 'rating', 'type': 'radio', 'id': 'star2', 'value': 2, }))
    # star3 = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'name': 'rating', 'type': 'radio', 'id': 'star3', 'value': 3, }))
    # star4 = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'name': 'rating', 'type': 'radio', 'id': 'star4', 'value': 4, }))
    # star5 = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'name': 'rating', 'type': 'radio', 'id': 'star5', 'value': 5, }))

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'email',
            'body',
            Div(HTML('<span>Your Rating: </span>'),
                Div('star',
                    css_class='stars'),
                HTML('{% csrf_token %}'),
                Submit('Submit', 'submit', css_class="primary-btn"),
                css_class='input-rating'
            ))
