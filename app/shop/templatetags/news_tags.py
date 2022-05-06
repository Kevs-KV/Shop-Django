from django import template

from cart.cart import Cart
from shop.models import Category

register = template.Library()


@register.simple_tag(takes_context=True, name='get_cart')
def get_cart(context):
    request = context['request']
    return Cart(request)

@register.simple_tag(name='get_category')
def get_category():
    return Category.objects.all()