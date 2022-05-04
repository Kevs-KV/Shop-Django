from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=100)
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
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'
        ordering = ('order',)
