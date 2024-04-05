from django.contrib import admin
from django import forms
from .models import Order, OrderItem, ServiceItem

class ServiceItemForm(forms.ModelForm):
    class Meta:
        model = ServiceItem
        fields = '__all__'
        widgets = {
            'service': forms.Textarea(attrs={'cols': 50, 'rows': 2}),
        }

class ServiceItemInline(admin.TabularInline):
    model = ServiceItem
    form = ServiceItemForm
    extra = 0
    can_delete = True

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['get_total']
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'order_total']
    readonly_fields = ['order_total']
    inlines = [OrderItemInline, ServiceItemInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_total()

admin.site.register(Order, OrderAdmin)


