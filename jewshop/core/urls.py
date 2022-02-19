from django.urls import path, include
from .views import *


urlpatterns = [
    path('catalog/', JewelryCatalog.as_view()),
]