from django.urls import path, include
from .views import *


urlpatterns = [
    path('catalog/', JewelryCatalog.as_view(), name='catalog'),
    path('jewelries/<slug:jew_slug>/', JewelryView.as_view(), name='jewelries'),
    path('', Home.as_view(), name='home')
]