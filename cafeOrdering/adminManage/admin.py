from django.contrib import admin
from .models import ManageInvoice

class ManageInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_reference', 'invoice_date', 'invoice_sent_date', 'invoice_total', 'invoice_paid')
    list_filter = ('invoice_date', 'invoice_sent_date', 'invoice_paid')
    search_fields = ('invoice_reference',)
    readonly_fields = ('invoice_sent_date',)

admin.site.register(ManageInvoice, ManageInvoiceAdmin)