from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from core.models import Metal, Material, Category, Jewelry, Review


class TestWalkPage(StaticLiveServerTestCase):
    def setUp(self):
        self.metal1 = Metal.objects.create(title="met1", slug="met1_slug")
        self.metal2 = Metal.objects.create(title="met2", slug="met2_slug")
        self.material1 = Material.objects.create(title="mat1", slug="mat1_slug", image="1.jpg")
        self.material2 = Material.objects.create(title="mat2", slug="mat2_slug", image="2.jpg")
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

        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def tearDown(self):
        self.browser.quit()



