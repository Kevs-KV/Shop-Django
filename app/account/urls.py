from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path

from account.views import ViewInfoUser, ViewCreateUser, ViewLoginUser

app_name = 'account'

urlpatterns = [
    path('login/', ViewLoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='shop:product_list'), name='logout'),
    path('user/info/', ViewInfoUser.as_view(), name='view_info_user'),
    path('user/create/', ViewCreateUser.as_view(), name='create_user')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
