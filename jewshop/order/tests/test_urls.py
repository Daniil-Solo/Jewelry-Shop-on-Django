from django.test import TestCase
from django.urls import reverse, resolve
from ..views import CreateOrderView, CreateOrderDoneView, check_order


class TestUrl(TestCase):
    def test_create_url_is_resolved(self):
        url = reverse('create_order')
        self.assertEquals(resolve(url).func.view_class, CreateOrderView)
        self.assertEquals('/order/create/', url)

    def test_create_done_url_is_resolved(self):
        url = reverse('create_order_done')
        self.assertEquals(resolve(url).func.view_class, CreateOrderDoneView)
        self.assertEquals('/order/done/', url)

    def test_check_order_url_is_resolved(self):
        url = reverse('check_order')
        self.assertEquals(resolve(url).func, check_order)
        self.assertEquals('/order/check/', url)
