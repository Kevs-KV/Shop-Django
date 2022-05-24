from django import forms

from wishlist.models import Wishlist


class WishlistAddProductForm(forms.Form):
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
