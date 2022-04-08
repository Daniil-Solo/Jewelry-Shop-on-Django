from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email',
                    'city', 'address', 'postal_code',
                    'created', 'paid', 'sent']
    list_filter = ['paid', 'sent', 'created']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)