from django.test import TestCase
from django.urls import reverse, resolve
from core.views import Home, JewelryCatalog, Search, JewelryView


class UrlTestCase(TestCase):

    def test_home_url(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, Home)
        self.assertEqual(url, '/')

    def test_catalog(self):
        url = reverse('catalog')
        self.assertEqual(resolve(url).func.view_class, JewelryCatalog)
        self.assertEqual(url, '/catalog/')

    def test_search(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func.view_class, Search)
        self.assertEqual(url, '/search/')

    def test_certain_jewelry(self):
        url = reverse('jewelries', args=['jewelry_slug'])
        self.assertEqual(resolve(url).func.view_class, JewelryView)
        self.assertEqual(url, '/jewelries/jewelry_slug/')
