from django.shortcuts import render
from django.views.generic import TemplateView
from core.utils import MenuMixin


def page_not_found_view(request, exception):
    return render(request, 'pages/404.html', status=404)


class PaymentView(TemplateView, MenuMixin):
    template_name = 'pages/payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_context = self.get_menu_context_data(title='Об оплате')
        return {**context, **menu_context}


class DeliveryView(TemplateView, MenuMixin):
    template_name = 'pages/delivery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_context = self.get_menu_context_data(title='О доставке')
        return {**context, **menu_context}


class AboutView(TemplateView, MenuMixin):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_context = self.get_menu_context_data(title='О нас')
        return {**context, **menu_context}