from django import template

from cart.cart import Cart
from shop.models import Category
from wishlist.models import Wishlist

register = template.Library()


@register.simple_tag(takes_context=True, name='get_cart')
def get_cart(context):
    request = context['request']
    return Cart(request)


@register.simple_tag(name='get_category')
def get_category():
    return Category.objects.all()


@register.simple_tag(takes_context=True, name='get_products_in_wishlist')
def get_amount_product(context):
    request = context['request']
    if request.user.is_authenticated:
        return len(
            Wishlist.objects.filter(user=request.user)
        )
    else:
        return '0'