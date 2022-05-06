from collections import namedtuple

from django.test import TestCase, Client
from django.urls import reverse

from ..views import CreateOrderView, CreateOrderDoneView, check_order
from core.models import Metal, Material, Jewelry, Category
from ..models import Order, OrderItem
RequestRecord = namedtuple('RequestRecord', ['session', ])


class TestCreateOrder(TestCase):
    def setUp(self):
        self.metal = Metal.objects.create(
            title="test_metal",
            slug="test_metal_slug",
        )
        self.material = Material.objects.create(
            title="test_material",
            slug="test_material_slug",
        )
        self.category = Category.objects.create(
            title="test_category",
            slug="test_category_slug",
        )
        self.jew = Jewelry.objects.create(
            title="test_jew",
            slug="test_jew_slug",
            description="test_jew_description",
            extra="test_jew_extra",
            is_in_stock=True,
            jew_cat=self.category,
            metal_cat=self.metal,
            price=100,
            quantity=5,
            main_photo="image.jpg",
        )
        self.jew.material_cats.add(self.material)
        self.client = Client()
        self.create_url = reverse('create_order')

    def test_create_order_GET(self):
        self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew.slug)))
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/create_order.html')
        self.assertEqual(response.context.get('title'), "Оформление заказа")

    def test_create_order_right_data_POST(self):
        self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew.slug)))
        response = self.client.post(self.create_url, {
            'full_name': 'Tester',
            'email': 'test@test.com',
            'phone': '7777777777',
            'city': 'Some_City',
            'address': 'some_street',
            'postal_code': 123242
        })
        order = Order.objects.last()
        self.assertEquals(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.items.first().product, self.jew)

        response = (self.client.get(reverse("create_order_done")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/create_order_done.html')
        self.assertEqual(response.context.get('title'), "Заказ оформлен")
        self.assertEqual(response.context.get('order_number'), 1)

    def test_create_order_empty_data_POST(self):
        self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew.slug)))
        response = self.client.post(self.create_url, {})
        self.assertEquals(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)


class TestCheckOrder(TestCase):
    successful_link = '/order/create/'
    unsuccessful_link = '/cart/'

    def setUp(self):
        self.metal = Metal.objects.create(
            title="test_metal",
            slug="test_metal_slug",
        )
        self.material = Material.objects.create(
            title="test_material",
            slug="test_material_slug",
        )
        self.category = Category.objects.create(
            title="test_category",
            slug="test_category_slug",
        )
        self.jew_1 = Jewelry.objects.create(
            title="test_jew",
            slug="test_jew_slug",
            is_in_stock=True,
            jew_cat=self.category,
            metal_cat=self.metal,
            price=100,
            quantity=1,
            main_photo="image.jpg",
        )
        self.jew_2 = Jewelry.objects.create(
            title="test_jew_2",
            slug="test_jew_slug_2",
            is_in_stock=True,
            jew_cat=self.category,
            metal_cat=self.metal,
            price=200,
            quantity=1,
            main_photo="image.jpg",
        )
        self.jew_1.material_cats.add(self.material)
        self.jew_2.material_cats.add(self.material)
        self.client = Client()
        self.check_url = reverse('check_order')

    def test_check_right_data(self):
        self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew_1.slug)))
        self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew_2.slug)))
        response = self.client.get(self.check_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.successful_link)

    def test_cart_contains_not_actual_quantities(self):
        self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew_1.slug)))
        self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew_2.slug)))
        self.jew_1.quantity = 0
        self.jew_1.save()
        response = self.client.get(self.check_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.unsuccessful_link)

    def test_product_has_removed_from_db(self):
        self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew_1.slug)))
        self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew_2.slug)))
        self.jew_1.delete()
        response = self.client.get(self.check_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.unsuccessful_link)

    def test_product_is_not_in_stock(self):
        self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew_1.slug)))
        self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew_2.slug)))
        self.jew_1.is_in_stock = False
        self.jew_1.save()
        response = self.client.get(self.check_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.unsuccessful_link)