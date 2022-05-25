from django.contrib.auth.models import User
from django.db import models

from shop.models import Product


class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE)


    class Meta:
        ordering = ('user',)
