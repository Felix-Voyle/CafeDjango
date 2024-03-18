from django import template

register = template.Library()

@register.filter(name='viewed')
def viewed(enquiry):
    return enquiry.viewed

@register.filter(name='unread')
def unread(enquiry):
    return not enquiry.viewed

@register.filter(name='filter_unread')
def filter_unread(enquiries):
    return enquiries.filter(viewed=False)
