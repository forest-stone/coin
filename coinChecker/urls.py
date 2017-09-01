from django.conf.urls import url

#from .views import stockListAPIView

from .views import (
    returnTicker,
    return24Volume,
)

urlpatterns = [
    url(r'^returnTicker/$', returnTicker, name='returnTicker'),
    url(r'^return24Volume/$', return24Volume, name='return24Volume'),
]
