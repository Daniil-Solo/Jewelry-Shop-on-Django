from django.urls import path
from .views import PaymentView, DeliveryView


urlpatterns = [
    path('payment/', PaymentView.as_view(), name='payment'),
    path('delivery/', DeliveryView.as_view(), name='delivery')
]

