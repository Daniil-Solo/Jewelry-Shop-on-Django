from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *


class JewelryCatalog(ListView):
    model = Jewelry
    template_name = "core/jewelry_catalog.html"
    context_object_name = "jewelries"

    def get_context(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Каталог"
        return context

    def get_queryset(self):
        jewelries = self.model.objects.all()
        filters = self.request.GET.dict()
        if filters:
            if filters.get("category"):
                params = filters["category"].split("_")
                print(params)
                jewelries = jewelries.filter(jew_cat__slug__in=params)
            if filters.get("metal"):
                params = filters["metal"].split("_")
                jewelries = jewelries.filter(metal_cat__slug__in=params)
                print(params)
            if filters.get("material"):
                params = filters["material"].split("_")
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
        return jewelries
