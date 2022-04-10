from jewshop.settings import CART_SESSION_ID
from core.models import Jewelry


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart
        if 'forced_to_update' not in self.cart:
            self.cart['forced_to_update'] = False

    def is_not_empty(self):
        jewelry_slugs = set(self.cart.keys())
        jewelry_slugs.remove('forced_to_update')
        return len(jewelry_slugs) > 0

    def set_forced_to_update(self, value):
        self.cart['forced_to_update'] = value
        self.save()

    def forced_to_update(self):
        return self.cart['forced_to_update']

    def add(self, jewelry):
        jewelry_slug = jewelry.slug
        if jewelry_slug not in self.cart:
            self.cart[jewelry_slug] = {
                'quantity': 0,
                'price': jewelry.price
            }
        self.cart[jewelry_slug]['quantity'] += 1
        self.save()

    def set_quantity(self, jewelry, new_quantity):
        jewelry_slug = jewelry.slug
        self.cart[jewelry_slug] = {
            'quantity': new_quantity,
            'price': jewelry.price
        }
        self.save()

    def save(self):
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, jewelry):
        jewelry_slug = jewelry.slug
        if jewelry_slug in self.cart:
            del self.cart[jewelry_slug]
            self.save()

    def __iter__(self):
        jewelry_slugs = set(self.cart.keys())
        jewelry_slugs.remove('forced_to_update')
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
                price=float(self.cart[jew_slug]['price']),
                quantity=int(self.cart[jew_slug]['quantity']),
            )
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values() if type(item) != bool)

    def get_current_quantity(self, jewelry):
        jewelry_slug = jewelry.slug
        if jewelry_slug in self.cart:
            return self.cart[jewelry_slug]["quantity"]
        else:
            return 0

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.session.modified = True
