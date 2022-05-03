from django.urls import reverse


class MenuMixin:
    @staticmethod
    def get_menu_context_data(**kwargs):
        context = kwargs
        context["footer"] = [
            dict(title="Покупателям",
                 sub_items=[
                     dict(title="Новинки", url=reverse("home")+"#news", target="self"),
                     dict(title="Доставка", url=reverse("delivery"), target="self"),
                     dict(title="Оплата", url=reverse("payment"), target="self"),
                    ]
                 ),
            dict(title="Информация",
                 sub_items=[
                     dict(title="О нас", url=reverse("about"), target="self"),
                     dict(title="Отзывы", url=reverse("home")+"#reviews", target="self"),
                    ]
                 ),
            dict(title="Контакты",
                 sub_items=[
                     dict(title="Вконтакте", url="https://vk.com/fragilemystery", target="blank"),
                     dict(title="Instagram", url="https://www.instagram.com/fragilemystery/", target="blank"),
                     dict(title="Telegram", url="https://t.me/fragilemystery", target="blank"),
                    ]
                 ),
        ]
        return context
