from django import template

register = template.Library()

@register.filter(name='get_quantity')
def get_quantity(quantities, product_id):
    return quantities.get(product_id, 0)