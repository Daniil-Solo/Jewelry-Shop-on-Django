from django.urls import reverse


class MenuMixin:
    @staticmethod
    def get_menu_context_data(**kwargs):
        context = kwargs
        context["footer"] = [
            dict(title="Покупателям",
                 sub_items=[
                     dict(title="Доставка", url=reverse("catalog")),
                     dict(title="Оплата", url=reverse("catalog")),
                     dict(title="Уход", url=reverse("catalog")),
                    ]
                 ),
            dict(title="Информация",
                 sub_items=[
                     dict(title="О нас", url=reverse("catalog")),
                    ]
                 ),
            dict(title="Контакты",
                 sub_items=[
                     dict(title="Вконтакте", url="https://vk.com/fragilemystery"),
                     dict(title="Instagram", url="https://www.instagram.com/fragilemystery/"),
                     dict(title="Telegram", url="https://t.me/fragilemystery"),
                    ]
                 ),
        ]
        return context
