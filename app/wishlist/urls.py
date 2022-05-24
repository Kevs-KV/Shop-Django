from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


app_name = 'wishlist'


urlpatterns = [
    path('', views.ViewWishList.as_view(), name='wishlist'),
    path('add/<int:product_id>', views.WishlistCreate.as_view(), name='wishlist_add'),
    path('remove/<int:product_id>', views.WishlistDelete.as_view(), name='wishlist_remove')
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)