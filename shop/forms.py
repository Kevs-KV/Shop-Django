from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'type': 'text', 'placeholder': "Your Name"}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'type': 'email', 'placeholder': "Your Email"}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'input', 'placeholder': "Your Review"}))
    star1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'name': 'rating', 'type': 'radio', 'id': 'star1', 'value': 1, }))
    star2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'name': 'rating', 'type': 'radio', 'id': 'star2', 'value': 2, }))
    star3 = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'name': 'rating', 'type': 'radio', 'id': 'star3', 'value': 3, }))
    star4 = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'name': 'rating', 'type': 'radio', 'id': 'star4', 'value': 4, }))
    star5 = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'name': 'rating', 'type': 'radio', 'id': 'star5', 'value': 5, }))
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
