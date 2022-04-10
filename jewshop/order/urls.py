from django.urls import path
from .views import CreateOrderView, CreateOrderDoneView


urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create_order'),
    path('done/', CreateOrderDoneView.as_view(), name='create_order_done')
]