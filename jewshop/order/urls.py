from django.urls import path
from .views import CreateOrderView, CreateOrderDoneView, check_order


urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create_order'),
    path('done/', CreateOrderDoneView.as_view(), name='create_order_done'),
    path('check/', check_order, name='check_order')
]