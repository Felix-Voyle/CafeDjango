from django.contrib import admin
from .models import ManageInvoice

class ManageInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_reference', 'invoice_date', 'invoice_sent_date', 'invoice_total', 'invoice_paid', 'has_invoice_pdf')
    list_filter = ('invoice_date', 'invoice_sent_date', 'invoice_paid')
    search_fields = ('invoice_reference',)
    readonly_fields = ('invoice_sent_date', 'has_invoice_pdf')

    def has_invoice_pdf(self, obj):
        return bool(obj.invoice_pdf)
    has_invoice_pdf.boolean = True
    has_invoice_pdf.short_description = 'Has Invoice PDF'

admin.site.register(ManageInvoice, ManageInvoiceAdmin)