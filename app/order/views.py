# Create your views here.
from django.urls import reverse
from django.views.generic import FormView

from cart.cart import Cart
from order.forms import OrderForm
from order.models import Order, Item
from .tasks import order_created

class ViewCreateOrder(FormView):
    template_name = 'shop/checkout.html'
    model = Order
    form_class = OrderForm

    def get_cart(self):
        return Cart(self.request)

    def get_context_data(self, **kwargs):
        context = super(ViewCreateOrder, self).get_context_data(**kwargs)
        context['cart'] = self.get_cart()
        context['order_form'] = OrderForm
        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        order.save()
        cart = self.get_cart()
        for item in cart:
            Item.objects.create(order=order,
                                product=item['product'],
                                price=item['price'],
                                quantity=item['quantity'])
        order_created.delay(order.id, order.email)
        cart.clear()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('shop:product_list')
