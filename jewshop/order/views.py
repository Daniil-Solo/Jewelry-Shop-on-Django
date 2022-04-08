from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from core.models import Jewelry
from .models import OrderItem

from .forms import OrderForm
from cart.cart import Cart
from core.views import MenuMixin


class CreateOrderView(MenuMixin, CreateView):
    form_class = OrderForm
    template_name = 'order/create_order.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        menu_context = self.get_menu_context_data(title="Оформление заказа")
        return {**context, **menu_context}

    def form_valid(self, form):
        self.object = form.save()
        cart = Cart(self.request)
        for item in cart:
            product = item["product"]
            quantity = item["quantity"]
            price = item["price"]
            OrderItem.objects.create(order=self.object, product=product, quantity=quantity, price=price)
        return HttpResponseRedirect(self.get_success_url())
