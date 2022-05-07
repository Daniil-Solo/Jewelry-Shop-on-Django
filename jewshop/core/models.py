from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Jewelry(models.Model):
    title = models.CharField(max_length=200, verbose_name="заголовок")
    slug = models.SlugField(unique=True, max_length=210, verbose_name="слаг")

    description = models.TextField(null=True, blank=True, verbose_name="описание")
    extra = models.TextField(null=True, blank=True, verbose_name="дополнительно")
    is_in_stock = models.BooleanField(default=False, verbose_name="в наличии")

    jew_cat = models.ForeignKey(
        to="Category",
        on_delete=models.SET_DEFAULT,
        default="Нет категории",
        verbose_name="категория украшения"
    )
    material_cats = models.ManyToManyField(
        to="Material",
        verbose_name="материал",
    )
    metal_cat = models.ForeignKey(
        to="Metal",
        on_delete=models.SET_DEFAULT,
        default="Не указана фурнитура",
        verbose_name="фурнитура"
    )

    price = models.FloatField(verbose_name="цена")
    quantity = models.PositiveSmallIntegerField(verbose_name="количество", default=1)
    weight = models.FloatField(null=True, blank=True, verbose_name="вес")
    length = models.FloatField(null=True, blank=True, verbose_name="длина")
    width = models.FloatField(null=True, blank=True, verbose_name="ширина")

    date_create = models.DateField(auto_now_add=True, verbose_name="дата создания")
    date_edit = models.DateField(auto_now=True, verbose_name="дата редактирования")

    main_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name="главное фото")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('jewelries', kwargs={'jew_slug': self.slug})

    class Meta:
        verbose_name = "Украшение"
        verbose_name_plural = "Украшения"
        ordering = ["title"]


class Gallery(models.Model):
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name="изображение")
    jewelry = models.ForeignKey(to="Jewelry", on_delete=models.CASCADE, related_name='images', verbose_name="украшение")

    class Meta:
        verbose_name = "Галерея"
        verbose_name_plural = "Галереи"
        ordering = ["jewelry"]

    def __str__(self):
        return f'Фото для {self.jewelry.title}'


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name="название")
    slug = models.SlugField(unique=True, max_length=50, verbose_name="слаг")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["title"]


class Material(models.Model):
    title = models.CharField(max_length=50, verbose_name="название")
    slug = models.SlugField(unique=True, max_length=50, verbose_name="слаг")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"
        ordering = ["title"]


class Metal(models.Model):
    title = models.CharField(max_length=50, verbose_name="название")
    slug = models.SlugField(unique=True, max_length=50, verbose_name="слаг")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фурнитура"
        verbose_name_plural = "Фурнитура"
        ordering = ["title"]


class Review(models.Model):
    title = models.CharField(max_length=50, verbose_name="название")
    stars = models.SmallIntegerField(
        verbose_name="оценка",
        validators=(
            MaxValueValidator(
                limit_value=5
            ),
            MinValueValidator(
                limit_value=1
            ),
        ),
        default=5,
    )
    text = models.TextField(null=True, blank=True, verbose_name='текст')
    date_create = models.DateField(auto_now_add=True, verbose_name="дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-date_create"]

    def __str__(self):
        return "Отзыв от клиента " + str(self.title)
