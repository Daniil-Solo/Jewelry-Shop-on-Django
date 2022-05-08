import datetime
import tempfile
from django.test import TestCase
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
        jew_in_stock_last.date_create = str(datetime.date.today() + datetime.timedelta(days=1))
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
        review_last.date_create = str(datetime.date.today() + datetime.timedelta(days=1))
        review_last.save()
        context_reviews = self.client.get(reverse('home')).context.get('reviews')
        self.assertIn(self.review, context_reviews[0])
        self.assertIn(review_last, context_reviews[0])
        self.assertEqual(context_reviews[0][0].title, 'test_review_2')
        self.assertEqual(context_reviews[0][1].title, 'test_review')


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
        self.assertContains(response, 'В наличии')
        self.assertContains(response, str(self.jew.metal_cat).capitalize())
        for material_cat in self.jew.material_cats.all():
            self.assertContains(response, str(material_cat).capitalize())


class CatalogTestCase(TestCase):
    def setUp(self):
        self.metal1 = Metal.objects.create(title="met1", slug="met1_slug")
        self.metal2 = Metal.objects.create(title="met2", slug="met2_slug")
        self.material1 = Material.objects.create(title="mat1", slug="mat1_slug")
        self.material2 = Material.objects.create(title="mat2", slug="mat2_slug")
        self.category1 = Category.objects.create(title="cat1", slug="cat1_slug")
        self.category2 = Category.objects.create(title="cat2", slug="cat2_slug")

        self.jew1 = Jewelry.objects.create(
            title="jew1",
            slug="jew1_slug",
            price=100,
            is_in_stock=True,
            jew_cat=self.category1,
            metal_cat=self.metal1,
            main_photo="image.jpg"
        )
        self.jew1.material_cats.add(self.material1)
        self.jew2 = Jewelry.objects.create(
            title="jew2",
            slug="jew2_slug",
            price=200,
            is_in_stock=True,
            jew_cat=self.category1,
            metal_cat=self.metal2,
            main_photo="image.jpg"
        )
        self.jew2.material_cats.add(self.material2)
        self.jew2.material_cats.add(self.material1)
        self.jew3 = Jewelry.objects.create(
            title="jew3",
            slug="jew3_slug",
            price=150,
            is_in_stock=True,
            jew_cat=self.category2,
            metal_cat=self.metal1,
            main_photo="image.jpg"
        )
        self.jew3.material_cats.add(self.material2)
        self.jew4 = Jewelry.objects.create(
            title="jew4",
            slug="jew4_slug",
            price=250,
            is_in_stock=True,
            jew_cat=self.category2,
            metal_cat=self.metal2,
            main_photo="image.jpg"
        )
        self.jew4.material_cats.add(self.material1)
        self.jew4.material_cats.add(self.material2)
        self.jew5 = Jewelry.objects.create(
            title="jew5",
            slug="jew5_slug",
            price=250,
            is_in_stock=False,
            jew_cat=self.category1,
            metal_cat=self.metal1,
            main_photo="image.jpg"
        )
        self.jew5.material_cats.add(self.material1)

    def test_init_catalog(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/jewelry_catalog.html')
        self.assertEqual(len(response.context.get('jewelries')), 5)

    def test_catalog_with_jewelries_in_stock(self):
        response = self.client.get(reverse('catalog'), dict(in_stock=1))
        self.assertEqual(len(response.context.get('jewelries')), 4)

    def test_catalog_with_jewelries_not_in_stock(self):
        response = self.client.get(reverse('catalog'), dict(in_stock=0))
        self.assertEqual(len(response.context.get('jewelries')), 1)

    def test_catalog_with_certain_metal(self):
        response = self.client.get(reverse('catalog'), dict(metal=self.metal1.slug))
        self.assertEqual(len(response.context.get('jewelries')), 3)

    def test_catalog_with_certain_category(self):
        response = self.client.get(reverse('catalog'), dict(category=self.category1.slug))
        self.assertEqual(len(response.context.get('jewelries')), 3)

    def test_catalog_with_several_certain_materials(self):
        response = self.client.get(reverse('catalog'), dict(material=[self.material1.slug, self.material2.slug]))
        self.assertEqual(len(response.context.get('jewelries')), 5)

    def test_catalog_with_one_certain_material(self):
        response = self.client.get(reverse('catalog'), dict(material=self.material1.slug))
        self.assertEqual(len(response.context.get('jewelries')), 4)

    def test_catalog_with_several_filters(self):
        response = self.client.get(reverse('catalog'), {
            'in_stock': 1,
            'category': self.category1.slug
        })
        self.assertEqual(len(response.context.get('jewelries')), 2)

    def test_catalog_with_several_filters_2(self):
        response = self.client.get(reverse('catalog'), {
            'in_stock': 0,
            'metal': self.metal2.slug
        })
        self.assertEqual(len(response.context.get('jewelries')), 0)

    def test_catalog_with_several_filters_3(self):
        response = self.client.get(reverse('catalog'), {
            'material': [self.material1.slug],
            'metal': self.metal2.slug,
            'category': self.category1.slug
        })
        self.assertEqual(len(response.context.get('jewelries')), 1)


class SearchViewTestCase(TestCase):
    def setUp(self):
        self.metal1 = Metal.objects.create(title="met1", slug="met1_slug")
        self.category1 = Category.objects.create(title="cat1", slug="cat1_slug")
        self.jew1 = Jewelry.objects.create(
            title="jew_1",
            slug="jew1_slug",
            price=200,
            jew_cat=self.category1,
            metal_cat=self.metal1,
            main_photo="image.jpg"
        )
        self.jew1 = Jewelry.objects.create(
            title="super_jew_2",
            slug="jew2_slug",
            price=200,
            jew_cat=self.category1,
            metal_cat=self.metal1,
            main_photo="image.jpg"
        )
        self.jew1 = Jewelry.objects.create(
            title="super_jew_3",
            slug="jew3_slug",
            price=200,
            jew_cat=self.category1,
            metal_cat=self.metal1,
            main_photo="image.jpg"
        )

    def test_init_search(self):
        response = self.client.get(reverse('search'), data=dict(q=''))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/jewelry_search.html')
        self.assertEqual(len(response.context.get('jewelries')), 3)

    def test_empty_result(self):
        response = self.client.get(reverse('search'), data=dict(q='some_query'))
        self.assertEqual(len(response.context.get('jewelries')), 0)

    def test_only_one_result(self):
        response = self.client.get(reverse('search'), data=dict(q='1'))
        self.assertEqual(len(response.context.get('jewelries')), 1)

    def test_full_match(self):
        response = self.client.get(reverse('search'), data=dict(q='jew_1'))
        self.assertEqual(len(response.context.get('jewelries')), 1)

    def test_several_results(self):
        response = self.client.get(reverse('search'), data=dict(q='super'))
        self.assertEqual(len(response.context.get('jewelries')), 2)