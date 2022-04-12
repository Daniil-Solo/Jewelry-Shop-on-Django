from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView
from core.models import Jewelry
from .models import OrderItem, Order

from .forms import OrderForm
from cart.cart import Cart
from core.views import MenuMixin


def check_order(request):
    cart = Cart(request)
    cart.set_forced_to_update(False)
    for item in cart:
        product = item["product"]
        quantity = item["quantity"]
        real_quantity = product.quantity
        if quantity > real_quantity:
            cart.set_forced_to_update(True)
            print(real_quantity)
            if real_quantity == 0:
                cart.remove(product)
            else:
                cart.set_quantity(product, real_quantity)
    if cart.products_updated:
        return redirect('cart')
    else:
        return redirect('create_order')


class CreateOrderDoneView(MenuMixin, TemplateView):
    template_name = 'order/create_order_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['order_number'] = Order.objects.last()
        menu_context = self.get_menu_context_data(title="Заказ оформлен")
        return {**context, **menu_context}


class CreateOrderView(MenuMixin, CreateView):
    form_class = OrderForm
    template_name = 'order/create_order.html'
    success_url = reverse_lazy('create_order_done')

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
            product.quantity = product.quantity - quantity
            product.save()
        cart.clear()
        return HttpResponseRedirect(self.get_success_url())
