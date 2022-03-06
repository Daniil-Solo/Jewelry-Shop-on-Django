from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from core.models import Jewelry
from django.views.generic import TemplateView
from .cart import Cart
from .forms import CartAddJewelryForm
from core.utils import MenuMixin


@require_POST
def cart_add(request, jew_slug):
    cart = Cart(request)
    jewelry = get_object_or_404(Jewelry, slug=jew_slug)
    form = CartAddJewelryForm(request.POST)
    form.set_choices(jewelry.quantity)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            jewelry=jewelry,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )
    return redirect('cart')


def cart_remove(request, jew_slug):
    cart = Cart(request)
    jewelry = get_object_or_404(Jewelry, slug=jew_slug)
    cart.remove(jewelry)
    return redirect('cart')


class CartView(MenuMixin, TemplateView):
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart(self.request)
        menu_context = self.get_menu_context_data(title="Корзина")
        return {**context, **menu_context}
