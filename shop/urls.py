from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


app_name = 'shop'


urlpatterns = [
    path('', views.ViewProductList.as_view(), name='product_list'),
    path('<int:id>/<slug:slug>/', views.ViewProductDetail.as_view(), name='product_detail'),
    path('<int:id>/<slug:slug>/comments/<int:page_num>/', views.ViewCreateProductComment.as_view(), name='product_comment'),
    path('store', views.ViewProductListForCategory.as_view(), name='store')
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)