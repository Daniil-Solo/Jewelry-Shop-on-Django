import datetime
import tempfile
from django.urls import reverse
from core.models import Metal, Material, Category, Jewelry, Review, Gallery
from .test_models import Settings


class HomeViewTestCase(Settings):
    def test_url_and_template(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(url, '/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
        self.assertEqual(response.context.get('title'), 'Главная')

    def test_check_news(self):
        jew_not_in_stock = Jewelry.objects.create(
            title="test_jew_2",
            slug="test_jew_slug_2",
            jew_cat=self.category,
            metal_cat=self.metal,
            main_photo=tempfile.NamedTemporaryFile(suffix='.jpg').name,
            price=100,
        )
        jew_in_stock_last = Jewelry.objects.create(
            title="test_jew_3",
            slug="test_jew_slug_3",
            jew_cat=self.category,
            metal_cat=self.metal,
            is_in_stock=True,
            main_photo=tempfile.NamedTemporaryFile(suffix='.jpg').name,
            price=100,
        )
        jew_in_stock_last.date_create = str(datetime.date.today()+datetime.timedelta(days=1))
        jew_in_stock_last.save()
        context_jewelries = self.client.get(reverse('home')).context.get('jewelries')
        self.assertIn(self.jew, context_jewelries)
        self.assertIn(jew_in_stock_last, context_jewelries)
        self.assertNotIn(jew_not_in_stock, context_jewelries)
        self.assertEqual(context_jewelries[0].title, 'test_jew_3')
        self.assertEqual(context_jewelries[1].title, 'test_jew')

    def test_check_reviews(self):
        review_last = Review.objects.create(
            title="test_review_2",
            stars=5,
        )
        review_last.date_create = str(datetime.date.today()+datetime.timedelta(days=1))
        review_last.save()
        context_reviews = self.client.get(reverse('home')).context.get('reviews')
        self.assertIn(self.review, context_reviews)
        self.assertIn(review_last, context_reviews)
        self.assertEqual(context_reviews[0].title, 'test_review_2')
        self.assertEqual(context_reviews[1].title, 'test_review')


class JewelryDetailViewTestCase(Settings):
    def test_url_and_template(self):
        url = reverse('jewelries', kwargs=dict(jew_slug=self.jew.slug))
        response = self.client.get(url)
        self.assertEqual(url, f'/jewelries/{self.jew.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/jewelry_view.html')
        self.assertEqual(response.context.get('title'), self.jew.title)

    def test_check_add(self):
        quantity_for_add = 2
        for _ in range(quantity_for_add):
            self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew.slug)))
        url = reverse('jewelries', kwargs=dict(jew_slug=self.jew.slug))
        response = self.client.get(url)
        self.assertEqual(response.context.get('remain'), self.jew.quantity - quantity_for_add)
        self.assertEqual(response.context.get('in_cart'), quantity_for_add)

    def test_check_add_full(self):
        for _ in range(self.jew.quantity):
            self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew.slug)))
        url = reverse('jewelries', kwargs=dict(jew_slug=self.jew.slug))
        response = self.client.get(url)
        self.assertEqual(response.context.get('remain'), 0)
        self.assertEqual(response.context.get('in_cart'), self.jew.quantity)

    def test_check_remove(self):
        quantity_for_add = 3
        for _ in range(quantity_for_add):
            self.client.post(reverse('cart_add', kwargs=dict(jew_slug=self.jew.slug)))
        self.client.post(reverse('cart_remove', kwargs=dict(jew_slug=self.jew.slug)))
        url = reverse('jewelries', kwargs=dict(jew_slug=self.jew.slug))
        response = self.client.get(url)
        self.assertEqual(response.context.get('remain'), self.jew.quantity)
        self.assertEqual(response.context.get('in_cart'), 0)

    def test_check_gallery(self):
        image1 = Gallery.objects.create(image='img1.jpg', jewelry=self.jew)
        image2 = Gallery.objects.create(image='img2.jpg', jewelry=self.jew)
        url = reverse('jewelries', kwargs=dict(jew_slug=self.jew.slug))
        response = self.client.get(url)
        self.assertEqual(response.context.get('image_links'), [image1.image.url, image2.image.url])

    def test_check_tags(self):
        url = reverse('jewelries', kwargs=dict(jew_slug=self.jew.slug))
        response = self.client.get(url)
        if self.jew.is_in_stock:
            self.assertContains(response, 'В наличии')
        self.assertContains(response, str(self.jew.metal_cat).capitalize())
        for material_cat in self.jew.material_cats.all():
            self.assertContains(response, str(material_cat).capitalize())
