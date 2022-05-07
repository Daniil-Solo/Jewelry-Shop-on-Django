from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1


class JewelryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_in_stock", "jew_cat", "metal_cat",
                    "price", "get_image")
    search_fields = ('title', 'description')
    list_editable = ("title", "is_in_stock", "price", "jew_cat")
    list_filter = ("is_in_stock", "jew_cat", "material_cats", "metal_cat")
    prepopulated_fields = {'slug': ('title',)}
    inlines = [GalleryInline]
    save_on_top = True
    readonly_fields = ("get_image", )
    fieldsets = (
        (None, {
            "fields": (("title", "slug", "is_in_stock"),)
        }),
        (None, {
            "fields": (("description", "extra"),)
        }),
        (None, {
            "fields": (("jew_cat", "metal_cat", "material_cats"),)
        }),
        (None, {
            "fields": (("price", "quantity"),)
        }),
        ("Размеры", {
            "classes": ("collapse",),
            "fields": (("weight", "length", "width"),)
        }),
        (None, {
            "fields": (("main_photo", "get_image"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.main_photo.url} alt="Изображение отсутствует" width="50" height="auto">')
    get_image.short_description = "Изображение"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", 'slug')
    list_editable = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class MaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "title", 'slug')
    search_fields = ('title', )
    list_editable = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class MetalAdmin(admin.ModelAdmin):
    list_display = ("id", "title", 'slug')
    search_fields = ('title',)
    list_editable = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "text", "stars")
    search_fields = ("title",)
    list_filter = ("stars",)
    fields = (
        ("title", "stars"),
        ("text",)
    )

admin.site.register(Jewelry, JewelryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Metal, MetalAdmin)
admin.site.register(Review, ReviewAdmin)

admin.site.site_title = "Fragile Mystery"
admin.site.site_header = "Fragile Mystery"
