class MenuMixin:
    @staticmethod
    def get_menu_context_data(**kwargs):
        context = kwargs
        context["catalog"] = [
            dict(title="Все украшения", url="catalog"),
            dict(title="Материалы", url="catalog"),
            dict(title="Подвески", url="catalog"),
            dict(title="Браслеты", url="catalog"),
            dict(title="Серьги", url="catalog"),
            dict(title="Кольца", url="catalog"),
        ]
        context["for_buyers"] = [
            dict(title="Доставка", url="catalog"),
            dict(title="Оплата", url="catalog"),
            dict(title="Уход", url="catalog"),
            dict(title="FAQ", url="catalog"),
        ]
        context["info"] = [
            dict(title="О бренде", url="catalog"),
            dict(title="Контакты", url="catalog"),
        ]
        return context
