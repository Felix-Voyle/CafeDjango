from django import template
from django.utils import timezone

register = template.Library()

@register.filter(name='viewed')
def viewed(enquiry):
    return enquiry.viewed

@register.filter(name='unread')
def unread(enquiry):
    return not enquiry.viewed

@register.filter(name='filter_unread')
def filter_unread(enquiries):
    unread = enquiries.filter(viewed=False)
    return unread.count()

@register.filter(name="filter_due")
def filter_due(invoices):
    due_invoices = invoices.filter(invoice_paid=False, invoice_date__lte=timezone.now() - timezone.timedelta(days=30))
    return due_invoices.count()