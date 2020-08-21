from django.contrib import admin
from .models import Order, OrderLineProduct


class OrderLineProductAdminInline(admin.TabularInline):
    model = OrderLineProduct
    readonly_fields = ('lineproduct_total',)
    extra = 1


class OrderLineProductAdmin(admin.ModelAdmin):
    """OrderLineProduct model admin panel"""

    ordering = ('order',)


class OrderAdmin(admin.ModelAdmin):
    """Order model admin panel"""

    inlines = (OrderLineProductAdminInline,)

    ordering = ('-date',)

    readonly_fields = ('order_number', 'date', 'order_total',)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLineProduct, OrderLineProductAdmin)
