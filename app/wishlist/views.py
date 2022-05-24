from django.http import HttpResponseRedirect
# Create your views here.
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DeleteView

from shop.models import Product
from wishlist.models import Wishlist


class WishlistCreate(View):
    model = Wishlist

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['product_id'], available=True)
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("account:login"))
        if not Wishlist.objects.filter(user=self.request.user, product=product):
            Wishlist.objects.create(user=self.request.user, product=product)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class WishlistDelete(View):
    model = Wishlist

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['product_id'], available=True)
        Wishlist.objects.filter(user=self.request.user, product=product).delete()
        return HttpResponseRedirect(reverse("wishlist:wishlist"))


class ViewWishList(ListView):
    model = Wishlist
    template_name = 'wishlist/wishlist.html'

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
