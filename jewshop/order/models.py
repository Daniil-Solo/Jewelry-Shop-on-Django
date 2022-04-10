from django.db import models
from core.models import Jewelry


class Order(models.Model):
    full_name = models.CharField(max_length=250, verbose_name="ФИО")
    email = models.EmailField(verbose_name="Электронная почта")
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    city = models.CharField(max_length=100, verbose_name="Город")
    address = models.CharField(max_length=250, verbose_name="Адрес")
    postal_code = models.CharField(max_length=20, verbose_name="Почтовый индекс")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    paid = models.BooleanField(default=False, verbose_name="Оплачено")
    sent = models.BooleanField(default=False, verbose_name="Отправлено")

    class Meta:
        ordering = ('created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Jewelry, on_delete=models.CASCADE, related_name='order_items')
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title}"
