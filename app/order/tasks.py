from django.conf import settings
from django.core.mail import send_mail

from website.celery import app
from .models import Order


@app.task
def order_created(order_id, mail):
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order.\ Your order id is {}.'.format(order.first_name,
                                                                                                order.id)
    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, (mail,), fail_silently=False)
    return mail_sent
