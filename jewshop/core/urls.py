from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from .views import *


urlpatterns = [
    path('catalog/', JewelryCatalog.as_view(), name='catalog'),
    path('search/', Search.as_view(), name='search'),
    path('jewelries/<slug:jew_slug>/', JewelryView.as_view(), name='jewelries'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('core/images/favicon.ico'))),
    path('', Home.as_view(), name='home')
]