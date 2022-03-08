from django.db import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse
from ..models import Metal


class Settings(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.metal = Metal.objects.create(
            title="test_metal",
            slug="test_metal_slug",
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
