from django.http import HttpResponseRedirect
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from wishlist.models import Wishlist


class WishlistCreate(CreateView):
    model = Wishlist
    fields = ['product']

    def form_valid(self, form):
        wishlist = form.save(commit=False)
        wishlist.user = self.request.user
        wishlist.save()
        return HttpResponseRedirect(self.get_success_url())


class WishlistDelete(DeleteView):
    model = Wishlist
    success_url = reverse_lazy('wishlist')


class ViewWishList(ListView):
    model = Wishlist

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
