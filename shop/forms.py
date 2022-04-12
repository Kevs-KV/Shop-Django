from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML
from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    name = forms.CharField(label='Name',
                           widget=forms.TextInput(attrs={'class': 'input', 'type': 'text', 'placeholder': "Your Name"}))
    email = forms.CharField(label='Email', widget=forms.TextInput(
        attrs={'class': 'input', 'type': 'email', 'placeholder': "Your Email"}))
    body = forms.CharField(label='Body', widget=forms.Textarea(attrs={'class': 'input', 'placeholder': "Your Review"}))
    rating = forms.IntegerField(min_value=0, max_value=5)

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', 'rating')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'email',
            'body',
            Div(HTML('<span>Your Rating: </span>'
                     '<div class="stars">'
                     '<input id="star5" name="rating" value=5 type="radio"><label for="star5"></label>'
                     '<input id="star4" name="rating" value=4 type="radio"><label for="star4"></label>'
                     '<input id="star3" name="rating" value=3 type="radio"><label for="star3"></label>'
                     '<input id="star2" name="rating" value=2 type="radio"><label for="star2"></label>'
                     '<input id="star1" name="rating" value=1 type="radio"><label for="star1"></label>'
                     '</div>'
                     '{% csrf_token %}'
                     '<button class="primary-btn">Submit</button>'),
                css_class='input-rating'
                ))
