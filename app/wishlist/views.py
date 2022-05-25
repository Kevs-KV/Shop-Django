from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from shop.models import Product
from shop.templatetags.news_tags import get_amount_product
from wishlist.models import Wishlist


class WishlistCreate(View):
    model = Wishlist

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['product_id'], available=True)
        if not Wishlist.objects.filter(user=self.request.user, product=product):
            Wishlist.objects.create(user=self.request.user, product=product)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class WishlistDelete(View):
    model = Wishlist

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['product_id'], available=True)
        Wishlist.objects.filter(user=self.request.user, product=product).delete()
        return HttpResponseRedirect(reverse("wishlist:wishlist"))


class ViewWishList(ListView):
    model = Wishlist
    template_name = 'wishlist/wishlist.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
