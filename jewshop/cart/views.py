from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from core.models import Jewelry
from django.views.generic import TemplateView
from .cart import Cart
from core.utils import MenuMixin


def cart_add(request, jew_slug):
    cart = Cart(request)
    jewelry = get_object_or_404(Jewelry, slug=jew_slug)
    current_quantity = cart.get_current_quantity(jewelry)
    if not current_quantity or current_quantity < jewelry.quantity:
        cart.add(jew_slug)
    return redirect('jewelries', jew_slug)


def cart_remove(request, jew_slug):
    cart = Cart(request)
    cart.remove(jew_slug)
    return redirect('cart')


class CartView(MenuMixin, TemplateView):
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_context = self.get_menu_context_data(title="Корзина")
        return {**context, **menu_context}
