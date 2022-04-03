from django.urls import path
from .views import *


urlpatterns = [
    path('', Authorization.as_view(), name='authorization'),
]