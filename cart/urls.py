from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


app_name = 'cart'


urlpatterns = [
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)