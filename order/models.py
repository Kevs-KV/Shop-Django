from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    adress = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)
    creation_date = models.DateTimeField(verbose_name='creation date')
    checked_out = models.BooleanField(default=False, verbose_name='checked out')

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'
        ordering = ('-creation_date',)



class Item(models.Model):
    cart = models.ForeignKey(Order, verbose_name='cart', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity', default=1)
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='unit price')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='item',
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'
        ordering = ('cart',)

