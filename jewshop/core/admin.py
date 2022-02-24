from django.contrib import admin
from .models import *


class JewelryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_in_stock", "jew_cat", "metal_cat",
                    "price", "main_photo")
    search_fields = ('title', 'description')
    list_editable = ("is_in_stock",)
    list_filter = ("is_in_stock", "jew_cat", "material_cats", "metal_cat")


class GalleryAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "jewelry")
    list_filter = ("jewelry",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title",)


class MaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image", "description")
    search_fields = ('title', 'description')


class MetalAdmin(admin.ModelAdmin):
    list_display = ("id", "title",)
    search_fields = ('title',)


admin.site.register(Jewelry, JewelryAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Metal, MetalAdmin)
