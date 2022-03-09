import datetime
import tempfile
from django.urls import reverse
from ..models import Metal, Material, Category, Jewelry, Review
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
