from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['get_total']
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_total']
    readonly_fields = ['order_total']
    inlines = [OrderItemInline]

    def save_model(self, request, obj, form, change):
        obj.update_total()
        super().save_model(request, obj, form, change)

admin.site.register(Order, OrderAdmin)

