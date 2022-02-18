from django.db import models


class Jewelry(models.Model):
    title = models.CharField(max_length=200, verbose_name="заголовок")
    slug = models.SlugField(unique=True, max_length=100, verbose_name="слаг")

    description = models.TextField(null=True, blank=True, verbose_name="описание")
    extra = models.TextField(null=True, blank=True, verbose_name="дополнительно")
    is_in_stock = models.BooleanField(default=False, verbose_name="в наличии")

    jew_cat = models.ForeignKey(
        to="Category",
        on_delete=models.SET_DEFAULT,
        default="Нет категории",
        verbose_name="категория украшения"
    )
    material_cat = models.ManyToManyField(
        to="Material",
        verbose_name="материал"
    )
    metal_cat = models.ManyToManyField(
        to="Metal",
        verbose_name="фурнитура"
    )
    price = models.FloatField(verbose_name="цена")
    weight = models.FloatField(null=True, blank=True, verbose_name="вес")
    length = models.FloatField(null=True, blank=True, verbose_name="длина")
    width = models.FloatField(null=True, blank=True, verbose_name="ширина")

    date_create = models.DateField(auto_now_add=True, verbose_name="дата создания")
    date_edit = models.DateField(auto_now=True, verbose_name="дата редактирования")


class Gallery(models.Model):
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    jewelry = models.ForeignKey(to="Jewelry", on_delete=models.CASCADE, related_name='images')


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name="название")


class Material(models.Model):
    title = models.CharField(max_length=50, verbose_name="название")
    slug = models.SlugField(unique=True, max_length=50, verbose_name="слаг")
    image = models.ImageField(upload_to='materials/', max_length=100, verbose_name="изображение")
    description = models.TextField(null=True, blank=True, verbose_name="описание")


class Metal(models.Model):
    title = models.CharField(max_length=50, verbose_name="название")
