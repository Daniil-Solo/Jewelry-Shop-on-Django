import tempfile
from django.db import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse
from ..models import Metal, Material


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
