from django.views.generic import ListView, DetailView, TemplateView
from .models import *
from .utils import *
from django.db.models import Min, Max
from cart.cart import Cart


class Search(MenuMixin, ListView):
    model = Jewelry
    template_name = "core/jewelry_search.html"
    context_object_name = "jewelries"

    def get_queryset(self):
        return Jewelry.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_context = self.get_menu_context_data(title="Поиск украшений")
        context["q"] = self.request.GET.get('q')
        return {**context, **menu_context}


class Home(MenuMixin, TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["jewelries"] = (
            Jewelry
            .objects
            .only("title", "price", "main_photo", "slug")
            .filter(is_in_stock=1)
            .order_by("-date_create")[:3]
        )
        reviews = (
            Review
            .objects
            .only("title", "stars", "text")
        )
        context["reviews"] = []
        for idx, review in enumerate(reviews):
            if idx % 3 == 0:
                context["reviews"].append([review])
            else:
                context["reviews"][-1].append(review)
        menu_context = self.get_menu_context_data(title="Главная")
        return {**context, **menu_context}


class JewelryView(MenuMixin, DetailView):
    model = Jewelry
    template_name = "core/jewelry_view.html"
    slug_url_kwarg = "jew_slug"
    context_object_name = "jew"

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image_links"] = [gallery.image.url for gallery in context["jew"].images.all()]
        menu_context = self.get_menu_context_data(title=self.object.title)
        context["remain"] = self.object.quantity - Cart(self.request).get_current_quantity(self.object.slug)
        context["in_cart"] = self.object.quantity - context["remain"]
        return {**context, **menu_context}


class JewelryCatalog(MenuMixin, ListView):
    model = Jewelry
    template_name = "core/jewelry_catalog.html"
    context_object_name = "jewelries"

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_context = self.get_menu_context_data(title="Каталог")
        prices = Jewelry.objects.aggregate(min=Min("price"), max=Max("price"))
        context["min_price"] = prices.get("min") or 0
        context["max_price"] = prices.get("max") or 0
        context["categories"] = Category.objects.values("title", "slug")
        context["metals"] = Metal.objects.values("title", "slug")
        context["materials"] = Material.objects.values("title", "slug")
        context["old_filters"] = self.request.GET.dict()
        if context["old_filters"]:
            for key in context["old_filters"]:
                context["old_filters"][key] = self.request.GET.getlist(key)
        return {**context, **menu_context}

    def get_queryset(self):
        jewelries = self.model.objects.only("title", "price", "main_photo", "slug")
        filters = self.request.GET.dict()
        if filters:
            if filters.get("category"):
                params = self.request.GET.getlist('category')
                jewelries = jewelries.filter(jew_cat__slug__in=params)
            if filters.get("metal"):
                params = self.request.GET.getlist('metal')
                jewelries = jewelries.filter(metal_cat__slug__in=params)
            if filters.get("material"):
                params = self.request.GET.getlist('material')
                jewelries = jewelries.filter(material_cats__slug__in=params)
            if filters.get("min_price"):
                params = float(filters["min_price"])
                jewelries = jewelries.filter(price__gte=params)
            if filters.get("max_price"):
                params = float(filters["max_price"])
                jewelries = jewelries.filter(price__lte=params)
            if filters.get("in_stock"):
                params = bool(int(filters["in_stock"]))
                jewelries = jewelries.filter(is_in_stock__exact=params)
        return jewelries.distinct()
