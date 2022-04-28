from django import template

from cart.cart import Cart

register = template.Library()


@register.simple_tag(takes_context=True)
def get_cart(context):
    request = context['request']
    return Cart(request)
