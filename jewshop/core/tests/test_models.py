import tempfile
from django.db import IntegrityError
from django.test import TestCase
from ..models import Metal, Material, Category, Jewelry


class Settings(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.metal = Metal.objects.create(
            title="test_metal",
            slug="test_metal_slug",
        )
        cls.material = Material.objects.create(
            title="test_material",
            slug="test_material_slug",
            image=tempfile.NamedTemporaryFile(suffix='.jpg').name,
            description="test_material_description"
        )
        cls.category = Category.objects.create(
            title="test_category",
            slug="test_category_slug",
        )
        cls.jew = Jewelry.objects.create(
            title="test_jew",
            slug="test_jew_slug",
            description="test_jew_description",
            extra="test_jew_extra",
            is_in_stock=True,
            jew_cat=cls.category,
            metal_cat=cls.metal,
            price=100,
            quantity=5,
            main_photo=tempfile.NamedTemporaryFile(suffix='.jpg').name,
        )
        cls.jew.material_cats.add(cls.material)


class MetalTestCase(Settings):
    def test_model_parameters(self):
        self.assertEqual(self.metal._meta.get_field("title").max_length, 50)
        self.assertEqual(self.metal._meta.get_field("title").verbose_name, "название")
        self.assertEqual(self.metal._meta.get_field("slug").max_length, 50)
        self.assertEqual(self.metal._meta.get_field("slug").verbose_name, "слаг")

    def test_successful_creating(self):
        self.assertEqual(self.metal.title, "test_metal")
        self.assertEqual(self.metal.slug, "test_metal_slug")

    def test_unsuccessful_creating(self):
        metal_with_duplicated_slug = Metal(
            title="test_metal",
            slug="test_metal_slug",
        )
        with self.assertRaises(IntegrityError):
            metal_with_duplicated_slug.save()


class MaterialTestCase(Settings):
    def test_model_parameters(self):
        self.assertEqual(self.material._meta.get_field("title").max_length, 50)
        self.assertEqual(self.material._meta.get_field("title").verbose_name, "название")
        self.assertEqual(self.material._meta.get_field("slug").max_length, 50)
        self.assertEqual(self.material._meta.get_field("slug").verbose_name, "слаг")
        self.assertEqual(self.material._meta.get_field("image").verbose_name, "изображение")
        self.assertEqual(self.material._meta.get_field("image").max_length, 100)
        self.assertEqual(self.material._meta.get_field("image").upload_to, 'materials/')
        self.assertEqual(self.material._meta.get_field("description").verbose_name, "описание")
        self.assertEqual(self.material._meta.get_field("description").null, True)
        self.assertEqual(self.material._meta.get_field("description").blank, True)

    def test_successful_creating(self):
        self.assertEqual(self.material.title, "test_material")
        self.assertEqual(self.material.slug, "test_material_slug")
        self.assertEqual(self.material.description, "test_material_description")

    def test_unsuccessful_creating(self):
        material_with_duplicated_slug = Material(
            title="test_material",
            slug="test_material_slug",
        )
        with self.assertRaises(IntegrityError):
            material_with_duplicated_slug.save()


class CategoryTestCase(Settings):
    def test_model_parameters(self):
        self.assertEqual(self.category._meta.get_field("title").max_length, 50)
        self.assertEqual(self.category._meta.get_field("title").verbose_name, "название")
        self.assertEqual(self.category._meta.get_field("slug").max_length, 50)
        self.assertEqual(self.category._meta.get_field("slug").verbose_name, "слаг")

    def test_successful_creating(self):
        self.assertEqual(self.category.title, "test_category")
        self.assertEqual(self.category.slug, "test_category_slug")

    def test_unsuccessful_creating(self):
        category_with_duplicated_slug = Category(
            title="test_category",
            slug="test_category_slug",
        )
        with self.assertRaises(IntegrityError):
            category_with_duplicated_slug.save()


class JewelryTestCase(Settings):
    def test_model_parameters(self):
        self.assertEqual(self.jew._meta.get_field("title").max_length, 200)
        self.assertEqual(self.jew._meta.get_field("title").verbose_name, "заголовок")
        self.assertEqual(self.jew._meta.get_field("slug").max_length, 210)
        self.assertEqual(self.jew._meta.get_field("slug").verbose_name, "слаг")
        self.assertEqual(self.jew._meta.get_field("description").null, True)
        self.assertEqual(self.jew._meta.get_field("description").blank, True)
        self.assertEqual(self.jew._meta.get_field("description").verbose_name, "описание")
        self.assertEqual(self.jew._meta.get_field("extra").null, True)
        self.assertEqual(self.jew._meta.get_field("extra").blank, True)
        self.assertEqual(self.jew._meta.get_field("extra").verbose_name, "описание")
        self.assertEqual(self.jew._meta.get_field("is_in_stock").default, False)
        self.assertEqual(self.jew._meta.get_field("is_in_stock").verbose_name, "в наличии")
        self.assertEqual(self.jew._meta.get_field("jew_cat").default, "Нет категории")
        self.assertEqual(self.jew._meta.get_field("jew_cat").verbose_name, "категория украшения")
        self.assertEqual(self.jew._meta.get_field("material_cats").verbose_name, "материал")
        self.assertEqual(self.jew._meta.get_field("metal_cat").default, "Не указана фурнитура")
        self.assertEqual(self.jew._meta.get_field("metal_cat").verbose_name, "фурнитура")
        self.assertEqual(self.jew._meta.get_field("price").verbose_name, "цена")
        self.assertEqual(self.jew._meta.get_field("quantity").verbose_name, "количество")
        self.assertEqual(self.jew._meta.get_field("quantity").default, 1)
        self.assertEqual(self.jew._meta.get_field("weight").null, True)
        self.assertEqual(self.jew._meta.get_field("weight").blank, True)
        self.assertEqual(self.jew._meta.get_field("weight").verbose_name, "вес")
        self.assertEqual(self.jew._meta.get_field("length").null, True)
        self.assertEqual(self.jew._meta.get_field("length").blank, True)
        self.assertEqual(self.jew._meta.get_field("length").verbose_name, "длина")
        self.assertEqual(self.jew._meta.get_field("width").null, True)
        self.assertEqual(self.jew._meta.get_field("width").blank, True)
        self.assertEqual(self.jew._meta.get_field("width").verbose_name, "ширина")
        self.assertEqual(self.jew._meta.get_field("date_create").verbose_name, "дата создания")
        self.assertEqual(self.jew._meta.get_field("date_edit").verbose_name, "дата редактирования")
        self.assertEqual(self.jew._meta.get_field("main_photo").verbose_name, "главное фото")
        self.assertEqual(self.jew._meta.get_field("main_photo").max_length, 100)
        self.assertEqual(self.jew._meta.get_field("main_photo").upload_to, 'photos/%Y/%m/%d/')

    def test_successful_creating(self):
        self.assertEqual(self.jew.title, "test_jew")
        self.assertEqual(self.jew.slug, "test_jew_slug")
        self.assertEqual(self.jew.description, "test_jew_description")
        self.assertEqual(self.jew.extra, "test_jew_extra")
        self.assertEqual(self.jew.is_in_stock, True)
        self.assertEqual(self.jew.jew_cat, self.category)
        self.assertEqual(self.jew.metal_cat, self.metal)
        self.assertEqual(self.jew.price, 100)
        self.assertEqual(self.jew.quantity, 5)

    def test_unsuccessful_creating(self):
        jew_with_duplicated_slug = Jewelry(
            title="test_jew",
            slug="test_jew_slug",
            jew_cat=self.category,
            metal_cat=self.metal,
            price=100,
        )
        with self.assertRaises(IntegrityError):
            jew_with_duplicated_slug.save()

    def test_get_absolute_url(self):
        self.assertEqual(self.jew.get_absolute_url(), '/jewelries/test_jew_slug/')