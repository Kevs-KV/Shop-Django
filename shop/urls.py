from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


app_name = 'shop'


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('<int:id>/<slug:slug>/comments/<int:page_num>/', views.product_comment, name='product_comment'),
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)