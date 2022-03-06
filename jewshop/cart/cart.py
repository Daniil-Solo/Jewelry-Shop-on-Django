from jewshop.settings import CART_SESSION_ID
from core.models import Jewelry


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, jewelry, quantity=1, update_quantity=False):
        jewelry_slug = jewelry.slug
        if jewelry_slug not in self.cart:
            self.cart[jewelry_slug] = {
                'quantity': 0,
                'price': str(jewelry.price)
            }
        if update_quantity:
            self.cart[jewelry_slug]['quantity'] = quantity
        else:
            self.cart[jewelry_slug]['quantity'] += quantity
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
        jewelry_slugs = self.cart.keys()
        jewelries = (
            Jewelry
            .objects
            .only("title", "slug", "main_photo")
            .filter(slug__in=jewelry_slugs)
        )
        for jew in jewelries:
            self.cart[jew.slug]['product'] = jew
        for item in self.cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.session.modified = True
