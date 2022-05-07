from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'full_name', 'city', 'created', 'paid', 'sent')
    list_filter = ('paid', 'sent')
    inlines = [OrderItemInline]
    ordering = ('-created', )
    fields = (
        ("full_name",),
        ("email", "phone"),
        ("city", "address", "postal_code"),
        ("paid", "sent")
    )


admin.site.register(Order, OrderAdmin)