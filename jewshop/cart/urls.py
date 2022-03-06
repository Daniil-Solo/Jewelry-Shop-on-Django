from django.urls import path
from .views import *


urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/<slug:jew_slug>/', cart_add, name='cart_add'),
    path('remove/<slug:jew_slug>/', cart_remove, name='cart_remove'),
]