from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from account.views import LoginUser

app_name = 'account'

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
