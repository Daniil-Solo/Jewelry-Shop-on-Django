from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
from .utils import *


class JewelryCatalog(MenuMixin, ListView):
    model = Jewelry
    template_name = "core/jewelry_catalog.html"
    context_object_name = "jewelries"

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_context = self.get_menu_context_data(title="Каталог")
        return {**context, **menu_context}

    def get_queryset(self):
        jewelries = self.model.objects.select_related('jew_cat', 'metal_cat').values(
            "title", "price"
        )
        filters = self.request.GET.dict()
        if filters:
            if filters.get("category"):
                params = filters["category"].split(",")
                print(params)
                jewelries = jewelries.filter(jew_cat__slug__in=params)
            if filters.get("metal"):
                params = filters["metal"].split(",")
                jewelries = jewelries.filter(metal_cat__slug__in=params)
                print(params)
            if filters.get("material"):
                params = filters["material"].split(",")
                jewelries = jewelries.filter(material_cats__slug__in=params)
                print(params)
            if filters.get("min_price"):
                params = float(filters["min_price"])
                jewelries = jewelries.filter(price__gte=params)
                print(params)
            if filters.get("max_price"):
                params = float(filters["max_price"])
                jewelries = jewelries.filter(price__lte=params)
                print(params)
            if filters.get("in_stock"):
                params = bool(int(filters["in_stock"]))
                jewelries = jewelries.filter(is_in_stock__exact=params)
                print(params)
        return jewelries.distinct()
