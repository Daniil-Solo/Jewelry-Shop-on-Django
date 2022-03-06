from collections import namedtuple
from django.test import Client, TestCase
from django.urls import reverse
from core.models import *
from .cart import Cart
RequestRecord = namedtuple('RequestRecord', ['session', ])


class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.metal = Metal.objects.create(title="test_metal", slug="test_metal_slug")
        self.material = Material.objects.create(title="test_material", slug="test_material_slug", image="material.jpg")
        self.category = Category.objects.create(title="test_category", slug="test_category_slug")
        self.jew = Jewelry.objects.create(
            title="test_jew",
            slug="test_jew_slug",
            jew_cat=self.category,
            metal_cat=self.metal,
            price=100,
            quantity=5,
            main_photo="jew.jpg",
        )
        self.jew2 = Jewelry.objects.create(
            title="test_jew2",
            slug="test_jew2_slug",
            jew_cat=self.category,
            metal_cat=self.metal,
            price=100,
            quantity=5,
            main_photo="jew2.jpg",
        )
        self.jew.material_cats.add(self.material)
        self.jew2.material_cats.add(self.material)

    def test_initial_cart(self):
        self.client.get(reverse('home'))
        current_cart = self.client.session.get("cart")
        self.assertEqual(current_cart, {})

    def test_successful_add_jewelry_to_cart(self):
        response = self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew.slug)), {
            'quantity': 1
        })
        current_cart = self.client.session.get("cart")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(current_cart, {'test_jew_slug': {'price': '100.0', 'quantity': 1}})

    def test_successful_remove_jewelry_from_cart(self):
        self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew.slug)), {
            'quantity': 1
        })
        response = self.client.get(reverse('cart_remove', kwargs=dict(jew_slug=self.jew.slug)))
        current_cart = self.client.session.get("cart")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(current_cart, {})

    def test_only_empty_cart(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Корзина")
        self.assertTemplateUsed(response, "cart/cart.html")

    def test_cart_with_one_jewelry(self):
        old_price = self.jew.price
        self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew.slug)), {
            'quantity': 3
        })
        new_price = 200
        self.jew.price = new_price
        self.jew.save()
        self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew.slug)), {
            'quantity': 2
        })
        self.client.get(reverse('cart'))
        cart = Cart(RequestRecord(session=self.client.session))
        some_jew_in_cart = list(cart)[0]
        self.assertEqual(some_jew_in_cart.get("quantity"), 5)
        self.assertEqual(some_jew_in_cart.get("price"), old_price)
        self.assertEqual(some_jew_in_cart.get("total_price"), 5 * old_price)

    def test_cart_with_jewelries(self):
        self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew.slug)), {
            'quantity': 3
        })
        self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew2.slug)), {
            'quantity': 2
        })
        self.client.get(reverse('cart'))
        cart = Cart(RequestRecord(session=self.client.session))
        self.assertEqual(cart.get_total_price(), 5*self.jew.price)
