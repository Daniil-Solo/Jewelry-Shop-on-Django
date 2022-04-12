from jewshop.settings import CART_SESSION_ID, CART_FORCED_TO_UPDATE
from core.models import Jewelry


class Cart(object):
    """
    self.session - сессия клиента
    self.products - словарь товаров
    self.products_updated - флаг обновления корзины, связанного с отсутствием выбранных товаров в наличии
    """

    def __init__(self, request):
        self.session = request.session
        products = self.session.get(CART_SESSION_ID)
        cart_updated = self.session.get(CART_FORCED_TO_UPDATE)
        if not products:
            products = self.session[CART_SESSION_ID] = {}
        if not cart_updated:
            cart_updated = self.session[CART_FORCED_TO_UPDATE] = False
        self.products = products
        self.products_updated = cart_updated

    def is_not_empty(self) -> bool:
        """
        Возвращает True, если в корзине есть товары
        Возвращает False, если корзина пуста
        """
        return len(self.products) > 0

    def add(self, jewelry: Jewelry) -> None:
        """
        Добавляет одну единицу указанного товара в корзину
        """
        jewelry_slug = jewelry.slug
        if jewelry_slug not in self.products:
            self.products[jewelry_slug] = {
                'quantity': 0,
                'price': jewelry.price
            }
        self.products[jewelry_slug]['quantity'] += 1
        self.save()

    def set_quantity(self, jewelry: Jewelry, new_quantity: float) -> None:
        """
        Устанавливает число единиц указанного товара
        """
        jewelry_slug = jewelry.slug
        self.products[jewelry_slug] = {
            'quantity': new_quantity,
            'price': jewelry.price
        }
        self.save()

    def remove(self, jewelry: Jewelry):
        """
        Удаляет указанный товар из корзины
        """
        jewelry_slug = jewelry.slug
        if jewelry_slug in self.products:
            del self.products[jewelry_slug]
            self.save()

    def save(self) -> None:
        """
        Сохранение изменений в сессии клиента
        """
        self.session[CART_SESSION_ID] = self.products
        self.session.modified = True

    def clear(self) -> None:
        """
        Очистка корзины через очистку сессии
        """
        del self.session[CART_SESSION_ID]
        del self.session[CART_FORCED_TO_UPDATE]
        self.session.modified = True

    def __iter__(self):
        """
        Перебор товаров в корзине
        Дополнительно к элементу добавляется ссылка на объект в БД и общая стоимость продукта
        """
        jewelry_slugs = self.products.keys()
        jewelry_slugs = list(jewelry_slugs)
        jewelries = (
            Jewelry
                .objects
                .only("title", "slug", "main_photo")
                .filter(slug__in=jewelry_slugs)
        )
        for jew in jewelries:
            jew_slug = jew.slug
            item = dict(
                product=jew,
                price=float(self.products[jew_slug]['price']),
                quantity=int(self.products[jew_slug]['quantity']),
            )
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self) -> float:
        """
        Возвращает общую стоимость товаров в корзине
        """
        return sum(item['price'] * item['quantity'] for item in self.products.values())

    def get_current_quantity(self, jewelry: Jewelry) -> float:
        """
        Возвращает текущее количество данного товара в корзине
        """
        jewelry_slug = jewelry.slug
        if jewelry_slug in self.products:
            return self.products[jewelry_slug]["quantity"]
        else:
            return 0

    def set_forced_to_update(self, value: bool) -> None:
        """
        Изменяет значение флага обновления корзины в сессии
        """
        self.products_updated = value
        self.session[CART_FORCED_TO_UPDATE] = self.products_updated
        self.session.modified = True
