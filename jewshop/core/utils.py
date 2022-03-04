class MenuMixin:
    @staticmethod
    def get_menu_context_data(**kwargs):
        context = kwargs
        context["for_buyers"] = [
            dict(title="Доставка", url="catalog"),
            dict(title="Оплата", url="catalog"),
            dict(title="Уход", url="catalog"),
        ]
        context["info"] = [
            dict(title="О нас", url="catalog"),
        ]
        context["contacts"] = [
            dict(title="Вконтакте", url="https://vk.com/fragilemystery"),
            dict(title="Instagram", url="https://www.instagram.com/fragilemystery/"),
            dict(title="Telegram", url="https://t.me/fragilemystery"),
        ]
        return context
