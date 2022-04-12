from jewshop.settings import CART_SESSION_ID, CART_FORCED_TO_UPDATE
from core.models import Jewelry


class Cart(object):
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

    def is_not_empty(self):
        return len(self.products) > 0

    def set_forced_to_update(self, value):
        self.products_updated = value
        self.session[CART_FORCED_TO_UPDATE] = self.products_updated
        self.session.modified = True

    def forced_to_update(self):
        return self.products_updated

    def add(self, jewelry):
        jewelry_slug = jewelry.slug
        if jewelry_slug not in self.products:
            self.products[jewelry_slug] = {
                'quantity': 0,
                'price': jewelry.price
            }
        self.products[jewelry_slug]['quantity'] += 1
        self.save()

    def set_quantity(self, jewelry, new_quantity):
        jewelry_slug = jewelry.slug
        self.products[jewelry_slug] = {
            'quantity': new_quantity,
            'price': jewelry.price
        }
        self.save()

    def save(self):
        self.session[CART_SESSION_ID] = self.products
        self.session.modified = True

    def remove(self, jewelry):
        jewelry_slug = jewelry.slug
        if jewelry_slug in self.products:
            del self.products[jewelry_slug]
            self.save()

    def __iter__(self):
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

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.products.values())

    def get_current_quantity(self, jewelry):
        jewelry_slug = jewelry.slug
        if jewelry_slug in self.products:
            return self.products[jewelry_slug]["quantity"]
        else:
            return 0

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.session.modified = True
